#!/bin/bash

for energy in 13 14 50 100
do
    rivet -a JetPlots ~/jet*/event*/data2/${energy}_1000.hepmc3 -o ${energy}_1000.yoda --pwd
done
