#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"

namespace Rivet {

  class PtPlot : public Analysis {
  public:

    DEFAULT_RIVET_ANALYSIS_CTOR(PtPlot);

    void init() {
      // Project final state particles into the event
      const FinalState fs;
      declare(fs, "FS");
      FastJets j04(fs, FastJets::ANTIKT, 0.4);
       declare(j04, "Jets");

      // Book a histogram of particle pT, with 100 bins from 0 to 100 GeV
      book(_h["histPt"] ,"Pt", 100, 0.0, 100.0);
      book(_h["njets04"], "njets04", 20, 0, 20);
    }

    void analyze(const Event& event) {
      const FinalState& fs = applyProjection<FinalState>(event, "FS");

      const Jets j04 = apply<JetAlg>(event, "Jets").jetsByPt(20*GeV);  
         _h["njets04"]->fill(j04.size()); 

         if (j04.size()< 1) vetoEvent;

      //for (const Particle& p : fs.particles()) {
        // Fill the histogram with the particle pT (converted to GeV)
        _h["histPt"]->fill(j04[0].pT());  
      //}
    }

    void finalize() {
      // Normalize the histogram to the cross-section
      //normalize(_histPt);
    }

  map<string, Histo1DPtr> _h;

  };

  DECLARE_RIVET_PLUGIN(PtPlot);
}
