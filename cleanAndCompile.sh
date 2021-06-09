#!/bin/bash

make clean
cd ../../../SFrame
make clean
cd ../CMSSW_*/src/UHH2
cmsenv
cd ../../../SFrame
source setup.sh
make -j4
cd ../CMSSW_*/src/UHH2
make -j9
