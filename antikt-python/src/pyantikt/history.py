# Classes for history and sequences

from enum import Enum

from dataclasses import dataclass
from pyantikt.pseudojet import PseudoJet
from pyantikt.tiles import Tiling

class HistoryState(Enum):
    Original = -4
    Invalid = -3
    NonexistentParent = -2
    BeamJet = -1

@dataclass
class HistoryElement:
    # There is an unpleasant use of "magic numbers" here, so that
    # state flags are mixed up with indexes

    # Index in _history where first parent of this jet
    # was created (-1 if this jet is an
    # original particle)
    parent1: int = -1

    # index in _history where second parent of this jet
    # was created (-1 if this jet is an
    # original particle); BeamJet if this history entry
    # just labels the fact that the jet has recombined
    # with the beam)
    parent2: int = -1

    # index in _history where the current jet is
    # recombined with another jet to form its child. It
    # is -1 if this jet does not further
    # recombine.
    child: int = -1

    # index in the _jets vector where we will find the
    # PseudoJet object corresponding to this jet
    # (i.e. the jet created at this entry of the
    # history). NB: if this element of the history
    # corresponds to a beam recombination, then
    # jetp_index=Invalid.
    jetp_index: int = -1

    # the distance corresponding to the recombination
    # at this stage of the clustering.
    dij: float = 0.0

    # the largest recombination distance seen
    # so far in the clustering history.
    max_dij_so_far: float = 0.0


@dataclass
class ClusterSequence:
    # This contains the physical PseudoJets; for each PseudoJet one
    # can find the corresponding position in the _history by looking
    # at _jets[i].cluster_history_index()
    jets: list[PseudoJet]

    # This vector will contain the branching history; for each stage,
    # _history[i].jetp_index indicates where to look in the _jets
    # vector to get the physical PseudoJet."""
    history: list[HistoryElement]

    # PseudoJet tiling (only for the tiling algorithm)
    tiling: Tiling | None

    # Total energy of the event
    Qtot: float = 0.0


def initial_history(particles):
    """Initialise the clustering history in a standard way,
    Takes as input the list of stable particles as input
    Returns the history and the total event energy."""

    # This is going to be a list of HistoryElements
    history = []
    Qtot = 0.0

    for i, _ in enumerate(particles):
        # Add in order, so that HistoryElement[i] -> particle[i]
        history.append(HistoryElement(jetp_index=i))

        # get cross-referencing right from PseudoJets
        particles[i].cluster_history_index = i

        # determine the total energy in the event
        Qtot += particles[i].E

    return history, Qtot
