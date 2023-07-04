import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import BytesIO
import datetime

# Set the style of the visualization
sns.set(style='whitegrid')

# Specify the path to the input CSV file
csv_file = 'data.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file, header=0)  # Set header=0 to indicate that the file has headers

# Create a list of columns to plot against CO2 Emitted
columns_to_plot = ['Centre of Mass Energies', 'Number of Events', 'Code Run Time (s)', 'CPU Energy (kWh)', 'GPU Energy (kWh)', 'Ram Energy (kWh)', 'Energy Used (kWh)', 'Number of Particles', 'Average Eta Jet', 'Average Phi Jet', 'Average pT Jet', 'Time for analysis (s)']

# Generate a timestamp
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Loop through each column and create a scatter plot
for column in columns_to_plot:
    # Create a new figure and axes for each plot
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Create the scatter plot
    sns.scatterplot(x=column, y='Total Amount of CO2 Emitted (kg)', data=df, ax=ax)
    ax.set_title(f'CO2 Emitted vs {column} (Tiled)')
    for i in range(len(df)):
        plt.text(df[column][i], df['Total Amount of CO2 Emitted (kg)'][i], f"{df['Centre of Mass Energies'][i]}, {df['Number of Events'][i]}")
    
    # Adjust the layout
    plt.tight_layout()
    
    # Save the plot to a PNG file with a useful name and timestamp
    filename = f'co2_emitted_plot_{column}_Tiled_{timestamp}.png'
    plt.savefig(filename, format='png')
    
    # Print the filename for reference
    print(f"The plot for {column} has been saved as {filename}.")
    plt.close(fig)  # Close the figure to free up resources
    
# Specify the path to the input CSV file
csv_file = 'data2.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file, header=0)  # Set header=0 to indicate that the file has headers

# Create a list of columns to plot against CO2 Emitted
columns_to_plot = ['Centre of Mass Energies', 'Number of Events', 'Code Run Time (s)', 'CPU Energy (kWh)', 'GPU Energy (kWh)', 'Ram Energy (kWh)', 'Energy Used (kWh)', 'Number of Particles', 'Average Eta Jet', 'Average Phi Jet', 'Average pT Jet', 'Time for analysis (s)']

# Generate a timestamp
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Loop through each column and create a scatter plot
for column in columns_to_plot:
    # Create a new figure and axes for each plot
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Create the scatter plot
    sns.scatterplot(x=column, y='Total Amount of CO2 Emitted (kg)', data=df, ax=ax)
    ax.set_title(f'CO2 Emitted vs {column} (Basic)')
    for i in range(len(df)):
        plt.text(df[column][i], df['Total Amount of CO2 Emitted (kg)'][i], f"{df['Centre of Mass Energies'][i]}, {df['Number of Events'][i]}")
    # Adjust the layout
    plt.tight_layout()
    
    # Save the plot to a PNG file with a useful name and timestamp
    filename = f'co2_emitted_plot_{column}_Basic_{timestamp}.png'
    plt.savefig(filename, format='png')
    
    # Print the filename for reference
    print(f"The plot for {column} has been saved as {filename}.")
    plt.close(fig)  # Close the figure to free up resources