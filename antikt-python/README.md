# AntiKt-Python

This package is an implementation of the [AntiKt algorithm](https://arxiv.org/abs/0802.1189) in Python, with both a basic version and a tiled implementation by Graeme-A-Stewart. [Link](https://github.com/graeme-a-stewart/antikt-python)

There is a pure Python implementation and one using `numpy` plus `numba`.

This code is used in the CHEP 2023 Paper, *Polyglot Jet Finding*.

This code was modified by adding [CodeCarbon Package](https://github.com/mlco2/codecarbon) to measure the power usage of the antikt algorithm in basic mode and N2 mode by Akshat Gupta (The University of Manchester).

## Copyright

All files are Copyright (C) CERN & The University of Manchester, 2023 and provided under the Apache-2 license.

## Acknowledgements

The antikt N^2 tiled algorithm is adapted from ClusterSequence_Tiled_N2.cc c++ code 
from the Fastjet (<https://fastjet.fr>,  hep-ph/0512210,  arXiv:1111.6097).

The reimplementation of the algorithm by Philippe Gras in Julia was extremely
useful when developing this Python version (<https://github.com/grasph/AntiKt.jl>).

This python code is provided by Graeme A Stewart [link](https://github.com/graeme-a-stewart/antikt-python).
