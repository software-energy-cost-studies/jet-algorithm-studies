import matplotlib.pyplot as plt
import yoda
import os
import datetime
import numpy as np

# Define filenames
filenames = ["13_1000.yoda", "14_1000.yoda", "50_1000.yoda", "100_1000.yoda"]

# Variables to plot
variables = ['P_{T} [GeV]', '#phi', '#eta']
variables_names = {'P_{T} [GeV]': "Pt", '#phi': "phi", '#phi2' : "phi2", '#eta': "eta"}
# Get current timestamp for saving files
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Loop over variables
for var in variables:
    plt.figure()

    # Check if the variable is 'P_{T} [GeV]' and set y-axis scale to logarithmic if true
    if var == 'P_{T} [GeV]':
        plt.yscale('log')

    # Loop over filenames and plot data
    for filename in filenames:
        # Read YODA file
        ao = yoda.read(filename)

        # Extract the energy information from the filename
        energy = os.path.splitext(filename)[0].split('_')[0]

        # Construct histogram path
        histogram_path = f"/JetPlots/{var}"

        # Check if histogram exists in YODA file
        if histogram_path in ao:
            h = ao[histogram_path]
            # Calculate error bars
            errors = np.sqrt(h.yVals())
            # Plot data with error bars
            plt.errorbar(h.xEdges()[:-1], h.yVals(), yerr=errors, label=f"{energy} GeV", fmt='o')

    # Set plot properties
    plt.legend(title="Center of mass energy")
    var2 = var
    var = var.replace("#", "\\")
    plt.xlabel("$" + var + "$")
    if var == 'P_{T} [GeV]':
        plt.ylabel('$\log(Number of events)$')
    else:
        plt.ylabel('Number of events')
    plt.title(f'Number of events vs ${var}$ for 1000 Events')

    # Save figure
    plt.savefig(f"{variables_names[var2]}_{timestamp}.png")

    # Show plot
    plt.show()
