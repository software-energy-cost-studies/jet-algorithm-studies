#! /usr/bin/env python3
"""Anti-Kt jet finder, Tiled N^2 version
   Can use numba and numpy for acceleration
"""

import argparse
import sys
import time
import logging
import os

from codecarbon import OfflineEmissionsTracker #Add CodeCarbon Offline Mode
from copy import deepcopy
from pathlib import Path

from pyantikt.hepmc import read_jet_particles

from pyantikt.benchmark import Benchmark

try:
    import pyantikt.acceleratedtiledjetfinder
except ImportError as e:
    print(f"pyantikt.acceleratedtiledjetfinder unavailable: {e}")
import pyantikt.tiledjetfinder


def main():
    parser = argparse.ArgumentParser(description="Tiled N^2 AntiKt Jet Finder")
    parser.add_argument(
        "--skip", type=int, default=0, help="Number of input events to skip"
    )
    parser.add_argument(
        "--maxevents",
        "-n",
        type=int,
        default=1,
        help="Maximum number of events to process",
    )
    parser.add_argument(
        "--trials", type=int, default=1, help="Number of trials to repeat"
    )
    parser.add_argument(
        "--numba", action="store_true", help="Run accelerated numba code version"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Activate logging debugging mode"
    )
    parser.add_argument(
        "--info", action="store_true", help="Activate logging info mode"
    )
    args = parser.parse_args(sys.argv[1:])

    if args.info:
        logger.setLevel(logging.INFO)
        logging.getLogger("jetfinder").setLevel(logging.INFO)
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logging.getLogger("jetfinder").setLevel(logging.DEBUG)

    # get all HEPMC3 Files in directory
    directory = '/mnt/d/summer-project/'  # Use the current directory

    hepmc_files = [filename for filename in os.listdir(directory) if filename.endswith('.hepmc3')]
    for file in hepmc_files:
        filenametemp = os.path.splitext(file)[0]  # Remove the file extension
        info = filenametemp.split('_')
        com = info[0]
        maxevents = info[1]
        if (args.maxevents != 1 and args.maxevents < maxevents):
            maxevents = args.maxevents
        if (int(maxevents) != 10000 and int(maxevents) != 100000):
            filename = "results/"+ filenametemp + "_tiled_carbon.csv"
            output = "results/"+filenametemp + "_tiled_benchmark.txt"
            logput = "results/"+filenametemp + "_tiled_log.txt"
            jetout = "results/"+filenametemp + "_tiled_jets.txt"
            logout = logging.FileHandler(logput, mode="w")
            logging.getLogger("jetfinder").addHandler(logout)
            benchmark_func(0.4, filename, file, output, args, int(maxevents), jetout)
            
def benchmark_func(cone_radius, filename, eventfile, output, args, maxevents, jetout):
    tracker = OfflineEmissionsTracker(save_to_file = True, country_iso_code="GBR", output_file=filename, tracking_mode="process") #GBR IS FOR UNITED KINGDOM 
    tracker.start()
    # Switch between implenentations here
    if args.numba:
        try:
            faster_tiled_N2_cluster = (
                pyantikt.acceleratedtiledjetfinder.faster_tiled_N2_cluster
            )
        except AttributeError as e:
            raise RuntimeError(
                "Numba accelerated code requested, but it's unavailable"
            ) from e
    else:
        faster_tiled_N2_cluster = pyantikt.tiledjetfinder.faster_tiled_N2_cluster

    original_events = read_jet_particles(
        file=eventfile, skip=args.skip, nevents=maxevents
    )

    benchmark = Benchmark(nevents=maxevents)
    fjet = open(jetout, "w")
    print("NFinaljets", file=fjet)
    # If we are bencmarking the numba code, do a warm up run
    # to jit compile the accelerated code
    if args.trials > 1 and args.numba:
        print("Warm up run with first event to jit compile code")
        faster_tiled_N2_cluster(deepcopy(original_events[0]), Rparam=cone_radius, ptmin=0.5)
    fjet = open(jetout, "w")
    print("NFinaljets", file=fjet)
    for itrial in range(1, args.trials + 1):
        if args.trials > 1:
            events = deepcopy(original_events)
        else:
            events = original_events
        start = time.monotonic_ns() / 1000.0  # microseconds
        for ievt, event in enumerate(events, start=1):
            logger.info(f"Event {ievt} has {len(event)} particles")
            antikt_jets = faster_tiled_N2_cluster(event, Rparam=cone_radius, ptmin=5.0)
            logger.info(f"Event {ievt}, found {len(antikt_jets)} jets")
            for ijet, jet in enumerate(antikt_jets):
                logger.info(f"{ijet}, {jet.rap}, {jet.phi}, {jet.pt}")
            print(len(antikt_jets), file=fjet)
        end = time.monotonic_ns() / 1000.0
        benchmark.runtimes.append(end - start)
        print(f"Trial {itrial}. Processed {len(events)} events in {end-start:,.2f} us")
        print(f"Time per event: {(end-start)/len(events):,.2f} us")
    if args.trials > 1:
        mean, stddev = benchmark.get_stats()
        print(f"Mean time per event {mean:,.2f} ± {stddev:,.2f} us")

    tracker.stop()


if __name__ == "__main__":
    logger = logging.getLogger(Path(sys.argv[0]).name)
    logger.setLevel(logging.WARN)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(name)s: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logging.getLogger("jetfinder").addHandler(ch)

    main()
