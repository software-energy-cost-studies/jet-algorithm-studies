#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"

namespace Rivet {

  class PtPlot : public Analysis {
  public:

    DEFAULT_RIVET_ANALYSIS_CTOR(PtPlot);

    void init() {
      // Project final state particles into the event
      const FinalState fs;
      declare(fs, "FS");

      // Book a histogram of particle pT, with 100 bins from 0 to 100 GeV
      book(_histPt ,"Pt", 100, 0.0, 100.0);
    }

    void analyze(const Event& event) {
      const FinalState& fs = applyProjection<FinalState>(event, "FS");

      for (const Particle& p : fs.particles()) {
        // Fill the histogram with the particle pT (converted to GeV)
        _histPt->fill(p.pT() / GeV);
      }
    }

    void finalize() {
      // Normalize the histogram to the cross-section
      //normalize(_histPt);
    }

  private:
    Histo1DPtr _histPt;

  };

  DECLARE_RIVET_PLUGIN(PtPlot);
}
