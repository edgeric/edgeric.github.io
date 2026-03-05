
import argparse
import os
import pickle
import sys
from collections import defaultdict
from datetime import datetime
from threading import Thread

import gym
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import math
import time

from utils import *
import torch
import redis
from edgeric_agent import *

def compute_policy():
    flag = False # to be deleted
    weights = fixed_weights(flag)
    send_scheduling_weight(weights,flag)  #### send the scheduling control action to the RT-E2 agent which will then publish it to RAN
    value_algo = "Fixed Weights" 

def fixed_weights():
    ue_data = get_metrics_multi()   #### subscribe to RAN via the RT-E2 agent to receive metrics
    numues = len(ue_data)
    weights = np.zeros(numues * 2)
    RNTIs = list(ue_data.keys())

    for i in range(numues):
        # Store RNTI and corresponding weight
        weights[i*2+0] = RNTIs[i]
        weights[i*2+1] = 1/numues
    
    return weights

if __name__ == "__main__":

    while True:
        compute_policy()