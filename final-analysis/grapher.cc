#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/FinalState.hh"

namespace Rivet {

class JetPlots : public Analysis {
public:
    DEFAULT_RIVET_ANALYSIS_CTOR(JetPlots);

    void init() {
        const FinalState fs;
        declare(fs, "FS");

        FastJets fJets(fs, FastJets::ANTIKT, 0.4);
        declare(fJets, "Jets");

        // Booking histograms for pt, phi, eta with 100 bins
        book(_h["pt"], "P_{T} [GeV]", 100, 0, 1000);
        book(_h["phi"], "#phi", 25, 0, 2*M_PI);
        book(_h["eta"], "#eta", 25, -5, 5);
    }

    void analyze(const Event& event) {
        const Jets& jets = apply<FastJets>(event, "Jets").jetsByPt(Cuts::pT > 20*GeV);

        for (const Jet& jet : jets) {
            _h["pt"]->fill(jet.pT()/GeV);
            _h["phi"]->fill(jet.phi());
            //_h["phi2"]->fill(jet.phi());
            _h["eta"]->fill(jet.eta());
        }
    }

    void finalize() {
        // Normalize each histogram by the cross section
        //for (auto& hist : _h) {
            //scale(hist.second, crossSection()/sumOfWeights());
        //}
    }

private:
    map<string, Histo1DPtr> _h;

};

DECLARE_RIVET_PLUGIN(JetPlots);
}
