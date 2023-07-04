#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"

namespace Rivet {

  class JetAnalysis : public Analysis {
  public:

    DEFAULT_RIVET_ANALYSIS_CTOR(JetAnalysis);

    void init() {
      const FinalState fs;
      declare(fs, "FS");
      FastJets j04(fs, FastJets::ANTIKT, 0.4);
      declare(j04, "Jets");
    }

    void analyze(const Event& event) {
      const FinalState& fs = applyProjection<FinalState>(event, "FS");

      const Jets j04 = apply<JetAlg>(event, "Jets").jetsByPt(20*GeV);  

      if (j04.size()< 1) vetoEvent;

      _sumPt += j04[0].pT() / GeV;
      _sumPhi += j04[0].phi() / GeV;
      _sumEta += j04[0].eta() / GeV;
      _nPts += 1;
      _nParticles += fs.particles().size();

    }

    void finalize() {
      cout << "Average pT: " << _sumPt / _nPts << endl;
      cout << "Average Phi: " << _sumPhi / _nPts << endl;
      cout << "Average Eta: " << _sumEta / _nPts << endl;
      cout << "Number of Particles: " << _nParticles << endl;
    }

    double _sumPt = 0;
    double _sumPhi = 0;
    double _sumEta = 0;
    int _nPts = 0;
    int _nParticles = 0;

  };

  DECLARE_RIVET_PLUGIN(JetAnalysis);
}
