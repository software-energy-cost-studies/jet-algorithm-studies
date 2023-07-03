import math
import yoda
import matplotlib.pyplot as plt
import time

def main():
    # Load the first YODA file and access the histogram
    yodafile1 = yoda.read('OriginalData.yoda')
    hist1 = yodafile1['/PtPlot/Pt']

    # Load the second YODA file and access the histogram
    yodafile2 = yoda.read('Rivet.yoda')
    hist2 = yodafile2['/PtPlot/Pt']

    # Perform binning analysis
    # ... Add your binning analysis code here ...

    # Get bin edges and heights for the first histogram
    bin_edges1 = [bin.xMid() - bin.xWidth() / 2 for bin in hist1.bins()]
    bin_heights1 = [bin.height() for bin in hist1.bins()]

    # Get bin edges and heights for the second histogram
    bin_edges2 = [bin.xMid() - bin.xWidth() / 2 for bin in hist2.bins()]
    bin_heights2 = [bin.height() for bin in hist2.bins()]

    # Normalize bin heights
    #total_events1 = sum(bin_heights1)
    #bin_heights1_normalized = [height / total_events1 for height in bin_heights1]

    #total_events2 = sum(bin_heights2)
    #bin_heights2_normalized = [height / total_events2 for height in bin_heights2]

    # Create a histogram plot using matplotlib
    plt.bar(bin_edges1, bin_heights1, width=[bin.xWidth() for bin in hist1.bins()], label='Graeme', alpha=0.5)
    plt.bar(bin_edges2, bin_heights2, width=[bin.xWidth() for bin in hist2.bins()], label='Pythia', alpha=0.5)
    plt.xlabel("pT (GeV)")
    plt.ylabel("Number of Events")
    plt.legend()  # Show legend with labels

    # Take natural logarithm of y-axis values
    #plt.gca().set_yscale("log")
    #plt.ylim(bottom=1)  # Set lower limit to avoid zero values
    timestr = time.strftime("%Y%m%d-%H%M%S")
    # Save histogram as PNG image
    plt.savefig("histogram"+timestr+".png")

if __name__ == '__main__':
    main()
