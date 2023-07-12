import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Read the CSV file
data = pd.read_csv('machinevsprocess.csv', header=None)

# Extract x and y axis data
x = data.iloc[:, 0]  # Assuming the first column is the x-axis
y1 = data.iloc[:, 1]  # Assuming the second column is the first y-axis
y2 = data.iloc[:, 2]  # Assuming the third column is the second y-axis
y3 = data.iloc[:, 3]  # Assuming the third column is the second y-axis
y4 = data.iloc[:, 4]  # Assuming the third column is the second y-axis

# Create the plot
plt.plot(x, y1, marker='o', label='Basic - Scaphandre')
plt.plot(x, y2, marker='^', label='Basic - CodeCarbon')
plt.plot(x, y3, marker='^', label='Tiled - Scaphandre')
plt.plot(x, y4, marker='D', label='Tiled - CodeCarbon')

# Add labels and title
plt.xlabel('Centre of Mass Energy (TeV)')
plt.ylabel('Energy Usage (kWh)')
plt.title('Energy Usage for 1000 events using Python')

# Add legend
plt.legend()

# Save the plot
current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
plt.savefig(f"results/Events_EnergyUsage_Scaphandre_{current_time}_EX10000BASIC.png")

# Display the plot
plt.show()
