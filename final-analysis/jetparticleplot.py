import matplotlib.pyplot as plt
import yoda
import os
import datetime
import numpy as np

# Define filenames
filenames = ["13_1000_particlejet.yoda", "14_1000_particlejet.yoda", "50_1000_particlejet.yoda", "100_1000_particlejet.yoda"]

# Variables to plot
variables = ['Number of Jets', 'Number of Particles']
variables_names = {'num_jets': 'Number of Jets', 'num_particles': 'Number of Particles'}

# Get current timestamp for saving files
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Loop over variables
for var in variables:
    plt.figure()

    # Loop over filenames and plot data
    for filename in filenames:
        # Read YODA file
        ao = yoda.read(filename)

        # Extract the energy information from the filename
        energy = os.path.splitext(filename)[0].split('_')[0]

        # Construct histogram path
        histogram_path = f"/JetParticlePlots/{var}"

        # Check if histogram exists in YODA file
        if histogram_path in ao:
            h = ao[histogram_path]
            # Plot data
            
            errors = np.sqrt(h.yVals())
            plt.errorbar(h.xEdges()[:-1], h.yVals(), yerr=errors, label=f"{energy} GeV", fmt='o')

    # Set plot properties
    plt.legend(title="Center of mass energy")
    plt.xlabel(var)
    plt.ylabel("Number of events")
    plt.title(f"Number of events vs {var} for 1000 Events")

    # Save figure
    plt.savefig(f"{var}_{timestamp}.png")

    # Show plot
    plt.show()
