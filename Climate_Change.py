import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib.ticker import MaxNLocator
from matplotlib.cm import get_cmap



def draw_pie_chart(labels, sizes, title='Pie Chart', colors=None):
    """
    Draw a pie chart using Matplotlib.

    Parameters:
        labels (list): List of labels for each category.
        sizes (list): List of sizes for each category.
        title (str): Title of the pie chart.
        colors (list): List of colors for each category. If not provided, Matplotlib will use default colors.
    """
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.axis('equal')  # Set aspect ratio to be equal, ensuring that the pie is drawn as a circle.
    plt.title(title)
    plt.show()


def line_plot(x, y, xlabel, ylabel, title, labels):
    plt.style.use('tableau-colorblind10')
    plt.figure(figsize=(7, 5))
    for index in range(len(y)):
        plt.plot(x, y[index], label=labels[index],linestyle='--')
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=6))
    plt.xticks(rotation=90)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.savefig('Line_plot.jpg', dpi=500)
    plt.show()
    return


def barplot(dataframe,xlabel,ylabel,title):
    cmap = get_cmap('viridis')
    dataframe.plot(kind='bar', figsize=(10, 6),cmap=cmap)
    # Set plot labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig('barplot.jpg', dpi=500)
    plt.show()
    return
    
    
    
def get_data_for_countries(dataframe,countries,Year_to_start,Year_to_end):
    dataframe = dataframe.T
    dataframe = dataframe.drop(['Country Code','Indicator Name','Indicator Code'])
    dataframe.columns = dataframe.iloc[0]
    dataframe = dataframe.drop(['Country Name'])
    dataframe= dataframe.reset_index()
    dataframe['Years']= dataframe['index']
    dataframe = dataframe.drop('index',axis=1)
    dataframe= dataframe[(dataframe['Years']>=Year_to_start)&(dataframe['Years']<=Year_to_end)]
    selected_data = dataframe[countries]
    selected_data = selected_data.fillna(selected_data.iloc[:,:-1].mean())
    return selected_data


def create_heat_map(df,title,cmap='viridis'):

    # Calculate the correlation matrix
    correlation_matrix = df.corr()
    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 6))
    # Create a heatmap using Matplotlib's pcolormesh, focusing on positive correlations
    heatmap = ax.pcolormesh(correlation_matrix, cmap=cmap)
    # Add colorbar
    cbar = plt.colorbar(heatmap)
    for i in range(len(correlation_matrix.columns)):
        for j in range(len(correlation_matrix.columns)):
            ax.text(j + 0.5, i + 0.5, f'{correlation_matrix.iloc[i, j]:.2f}',
                    ha='center', va='center', color='white')

    # Set axis labels and title
    ax.set_xticks(range(len(correlation_matrix.columns)))
    ax.set_yticks(range(len(correlation_matrix.columns)))
    ax.set_xticklabels(correlation_matrix.columns, rotation=90)
    ax.set_yticklabels(correlation_matrix.columns)
    plt.title(title)
    plt.savefig('Heatmap_plot.jpg', dpi=500)
    # Display the plot
    plt.show()
    

def get_data_for_specific_country(data_frames,country_name,names,start_year,end_year):
    country_data = []
    for i, data in enumerate(data_frames):
        data = get_data_for_countries(data,country_name,start_year,end_year)
        data = data.rename(columns={country_name[0]:names[i]})
        country_data.append(data)
    country_data = pd.concat(country_data, axis= 1)
    country_data = country_data.T.drop_duplicates().T
    country_data = country_data.drop('Years',axis=1)
    return country_data


def convert_to_lists(df,cols):
    column_lists = [df[col].tolist() for col in cols[:-1]]
    return column_lists


def get_data_for_bar(df,years):
    df = df[df['Years'].isin(years)]
    df = df.set_index('Years')
    return df


def make_visulizations(dataframes,cols,start_year,end_year,names,years):
    line_plot(list(get_data_for_countries(dataframes[0], cols, start_year, end_year)['Years']),convert_to_lists(get_data_for_countries(dataframes[0], cols, start_year, end_year),cols), 'Years', 'Agricultural land', 'Agricultural land comparision in East Asia', cols[:-1])
    line_plot(list(get_data_for_countries(dataframes[1], cols, start_year, end_year)['Years']),convert_to_lists(get_data_for_countries(dataframes[1], cols, start_year, end_year),cols), 'Years', 'Urban Population', 'Urban Population comparision in East Asia', cols[:-1])
    barplot(get_data_for_bar(get_data_for_countries(dataframes[6],cols,start_year, end_year),years),'Years','Forest area','Forest Area Comparision of East Asian Countries')
    barplot(get_data_for_bar(get_data_for_countries(dataframes[3],cols,start_year, end_year),years),'Years',"Emission of CO2 ",'Emission of CO2 for East Asian Countries')
    country_name = ['Mongolia','Years']
    create_heat_map(get_data_for_specific_country(data_frames,country_name,names,start_year,end_year),'Japan','tab10')
    country_name = ['Thailand','Years']
    create_heat_map(get_data_for_specific_country(data_frames,country_name,names,start_year,end_year),'Thailand','RdPu')
    country_name = ['Singapore','Years']
    create_heat_map(get_data_for_specific_country(data_frames,country_name,names,start_year,end_year),'Singapore','tab20c')

total_population = pd.read_csv('total_population.csv', skiprows=4)
CO2_emission_ = pd.read_csv('CO2_emissions.csv', skiprows=4)
GDP_Data_ = pd.read_csv('GDP_of_Agriculture_forestry_and_fishing_value_added.csv', skiprows=4)
Urban_population = pd.read_csv('Urban_population.csv', skiprows=4)
Agricultural_land = pd.read_csv('Agricultural_land.csv', skiprows=4)
School_enrollment = pd.read_csv('School_enrollment.csv', skiprows=4)
Electric_power_consumption = pd.read_csv('Electric_power_consumption.csv', skiprows=4)
Forest_area = pd.read_csv('Forest_area.csv', skiprows=4)
countries = ['Malaysia','Thailand','Cambodia','Philippines','Mongolia','Years']
start_year = '1970'
end_year   = '2021'
years = ['1995','2000','2005','2010','2015','2020']
names = ['Agricultural_land','Urban_population','GDP_Data_','CO2_emission_','School_enrollment','Electric_power_consumption','Forest_area']
data_frames = [Agricultural_land,Urban_population,GDP_Data_,CO2_emission_,School_enrollment,Electric_power_consumption,Forest_area]
make_visulizations(data_frames,countries,start_year,end_year,names,years)

cols = ['Malaysia','Thailand','Cambodia','Philippines','Mongolia','Years']
table_data = get_data_for_countries(total_population,cols,'1970','2021')
table_data = get_data_for_bar(table_data,['1980','2020'])
table_data = table_data.T
table_data = table_data.round(1)
draw_pie_chart(table_data.index, table_data['1980'], title='Population Percentage of East Asia in 1980', colors=None)
draw_pie_chart(table_data.index, table_data['2020'], title='Population Percentage of East Asia in 2020', colors=None)



