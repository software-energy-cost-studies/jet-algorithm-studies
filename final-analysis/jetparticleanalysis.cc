#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/FinalState.hh"

namespace Rivet {

class JetParticlePlots : public Analysis {
public:
    DEFAULT_RIVET_ANALYSIS_CTOR(JetParticlePlots);

    void init() {
        const FinalState fs;
        declare(fs, "FS");

        FastJets fJets(fs, FastJets::ANTIKT, 0.4);
        declare(fJets, "Jets");

        // Booking histograms for number of jets and number of particles
        book(_h["num_jets"], "Number of Jets", 16, -1, 15);
        book(_h["num_particles"], "Number of Particles", 95, 50, 1000);
    }

    void analyze(const Event& event) {
        const Jets& jets = apply<FastJets>(event, "Jets").jetsByPt(Cuts::pT > 20*GeV);
        const Particles& particles = apply<FinalState>(event, "FS").particles();

        _h["num_jets"]->fill(jets.size());
        _h["num_particles"]->fill(particles.size());
    }

    void finalize() {
        // No normalization or additional processing required for this analysis
    }

private:
    std::map<std::string, Histo1DPtr> _h;

};

DECLARE_RIVET_PLUGIN(JetParticlePlots);
}
