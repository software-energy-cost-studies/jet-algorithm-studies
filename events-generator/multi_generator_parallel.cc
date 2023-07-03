#include "Pythia8/Pythia.h"
#ifndef HEPMC2
#include "Pythia8Plugins/HepMC3.h"
#else
#include "Pythia8Plugins/HepMC2.h"
#endif

#include <iostream>
#include <fstream>
#include <chrono>
#include <vector>
#include <string>

// Include OpenMP for multi-threading
#include <omp.h>

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
  //string filename = removeDecimalPlaces(energy) + "_" + to_string(numEvents) + "_" + removeDecimalPlaces(jetRadius) + ".hepmc3";
  string filename = removeDecimalPlaces(energy) + "_" + to_string(numEvents) + ".hepmc3";
  auto start = chrono::high_resolution_clock::now();
  // Interface for conversion from Pythia8::Event to HepMC event.
  // Specify the file where HepMC events will be stored.
  Pythia8::Pythia8ToHepMC topHepMC(filename);

  // Generator. Process selection. LHC initialization. Histogram.
  Pythia pythia;
  pythia.readString("Beams:eCM = " + to_string(energy * 1000.));
  pythia.readString("HardQCD:all = on");
  pythia.readString("PhaseSpace:pTHatMin = 20.");
  pythia.readString("JetMatching:coneRadius = " + to_string(jetRadius * 1.));
  cout << "JetMatching:coneRadius = " + to_string(jetRadius * 1.) << endl;
  pythia.init();

  // Begin event loop. Generate event. Skip if error.
  for (int iEvent = 0; iEvent < numEvents; ++iEvent) {
    if (!pythia.next()) continue;

    // Construct new empty HepMC event, fill it, and write it out.
    topHepMC.writeNextEvent(pythia);
  }
  auto end = chrono::high_resolution_clock::now();
  // Save the dataset filename and generation time to the file.
  outFile << filename << "," << chrono::duration_cast<chrono::seconds>(end - start).count() << endl;
}

int main() {
  // Parameters for dataset generation.
  vector<double> energies = {13.0, 14.0, 50.0, 100.0};  // TeV
  vector<int> numEvents = {100, 1000, 10000, 100000};
  vector<double> jetRadii = {0.7};

  // Open the output file to save the generation times in CSV format.
  ofstream timeFile("dataset_generation_times.csv");
  if (!timeFile.is_open()) {
    cerr << "Unable to open file: dataset_generation_times.csv" << endl;
    return 1;
  }

  // Write the header for the CSV file.
  timeFile << "Filename,Duration" << endl;

  // Generate datasets with varying parameters in parallel.
#pragma omp parallel for
  for (size_t i = 0; i < energies.size(); ++i) {
    for (size_t j = 0; j < numEvents.size(); ++j) {
      for (size_t k = 0; k < jetRadii.size(); ++k) {
        // Each thread operates on its own output stream
        ofstream threadOutFile;
        threadOutFile.open("temp_file_" + to_string(i) + "_" + to_string(j) + "_" + to_string(k) + ".csv");

        generateDataset(energies[i], numEvents[j], jetRadii[k], threadOutFile);

        // Close the thread-specific output file
        threadOutFile.close();
      }
    }
  }

  // Combine the temporary files into the final CSV file.
  for (size_t i = 0; i < energies.size(); ++i) {
    for (size_t j = 0; j < numEvents.size(); ++j) {
      for (size_t k = 0; k < jetRadii.size(); ++k) {
        ifstream threadInFile("temp_file_" + to_string(i) + "_" + to_string(j) + "_" + to_string(k) + ".csv");
        if (threadInFile.is_open()) {
          string line;
          while (getline(threadInFile, line)) {
            timeFile << line << endl;
          }
          threadInFile.close();
        }
      }
    }
  }

  // Remove the temporary files.
  for (size_t i = 0; i < energies.size(); ++i) {
    for (size_t j = 0; j < numEvents.size(); ++j) {
      for (size_t k = 0; k < jetRadii.size(); ++k) {
        string filename = "temp_file_" + to_string(i) + "_" + to_string(j) + "_" + to_string(k) + ".csv";
        remove(filename.c_str());
      }
    }
  }

  // Close the output file.
  timeFile.close();

  return 0;
}
