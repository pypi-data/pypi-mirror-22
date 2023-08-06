# -*- coding: utf-8 -*-
'''
Copyright (c) 2017 by Benjamin Manns
This file is part of Statistical Parameter Estimation Tool (SPOTPY).
:author: Benjamin Manns

This code shows you, how to use the hydroligcal signatures. They can also be implemented in the def objective function.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from spotpy.examples.spot_setup_hymod import spot_setup
import pandas as pd
import spotpy.signatures as sig

print("INFO: For this example you need the folder >hymod< in the examples folder")

spot_setup = spot_setup()
parameterset = spot_setup.parameters()['random']
simulation = spot_setup.simulation(parameterset)
observation = spot_setup.evaluation()

timespanlen = simulation.__len__()

print(sig.getMedianFlow(simulation, observation))
print(sig.getDuration(simulation, observation,pd.date_range("2015-05-01", periods=timespanlen),0.2))
print(sig.getBaseflowIndex(simulation, observation, pd.date_range("2015-05-01", periods=timespanlen)))
print(sig.getSlopeFDC(simulation, observation))
print(sig.getLowFlowVar(simulation, observation, pd.date_range("2015-05-01", periods=timespanlen)))
print(sig.getHighFlowVar(simulation, observation, pd.date_range("2015-05-01", periods=timespanlen)))
