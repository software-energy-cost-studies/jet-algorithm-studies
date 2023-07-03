#include "Pythia8/Pythia.h"
#ifndef HEPMC2
#include "Pythia8Plugins/HepMC3.h"
#else
#include "Pythia8Plugins/HepMC2.h"
#endif

#include <iostream>
#include <fstream>
#include <chrono>

using namespace Pythia8;
using namespace std;

std::string removeDecimalPlaces(double value) {
    std::string stringValue = std::to_string(value);
    stringValue.erase(stringValue.find_last_not_of('0') + 1, std::string::npos);
    if (stringValue.back() == '.')
        stringValue.pop_back();
    return stringValue;
}

void generateDataset(double energy, int numEvents, double jetRadius, ofstream& outFile) {
  // Construct the filename based on the input parameters.
  auto start = chrono::high_resolution_clock::now();
  string filename = removeDecimalPlaces(energy) + "_" + to_string(numEvents) + "_" + removeDecimalPlaces(jetRadius) + ".hepmc3";

  // Interface for conversion from Pythia8::Event to HepMC event.
  // Specify the file where HepMC events will be stored.
  Pythia8::Pythia8ToHepMC topHepMC(filename);

  // Generator. Process selection. LHC initialization. Histogram.
  Pythia pythia;
  pythia.readString("Beams:eCM = " + to_string(energy * 1000.));
  pythia.readString("HardQCD:all = on");
  pythia.readString("PhaseSpace:pTHatMin = 20.");
  pythia.readString("JetMatching:coneRadius = " + to_string(jetRadius * 1.));
  pythia.init();

  // Begin event loop. Generate event. Skip if error.
  //auto start = chrono::high_resolution_clock::now();
  for (int iEvent = 0; iEvent < numEvents; ++iEvent) {
    if (!pythia.next()) continue;

    // Construct new empty HepMC event, fill it, and write it out.
    topHepMC.writeNextEvent(pythia);
  }
  auto end = chrono::high_resolution_clock::now();
  auto duration = chrono::duration_cast<chrono::seconds>(end - start).count();
  //cout << "Dataset generation time: " << duration << " seconds" << endl;

  // Save the dataset filename to the file.
  outFile << filename << ":" << endl;
  outFile << "Dataset generation time: " << duration << " seconds" << endl;
}

int main() {
  // Parameters for dataset generation.
  vector<double> energies = {13.0, 14.0, 50.0, 100.0};  // TeV
  vector<int> numEvents = {100, 1000, 10000, 100000};
  vector<double> jetRadii = {0.4, 0.7, 1.0};

  // Open the output file to save the generation times.
  ofstream timeFile("dataset_generation_times.txt");
  if (!timeFile.is_open()) {
    cerr << "Unable to open file: dataset_generation_times.txt" << endl;
    return 1;
  }

  // Generate datasets with varying parameters.
  for (double energy : energies) {
    for (int events : numEvents) {
      for (double radius : jetRadii) {
        generateDataset(energy, events, radius, timeFile);
      }
    }
  }

  // Close the output file.
  timeFile.close();

  return 0;
}
