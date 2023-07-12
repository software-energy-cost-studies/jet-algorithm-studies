#!/bin/bash

for energy in 13 14 50 100
do
    rivet -a JetParticlePlots ~/jet*/event*/data2/${energy}_1000.hepmc3 -o ${energy}_1000_particlejet.yoda --pwd
done
