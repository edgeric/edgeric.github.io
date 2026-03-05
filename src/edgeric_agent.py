def send_control():
    """
    Composes and sends a control message to the RAN. This message contains
    data for the actions to be taken for each UE, identified by their RNTIs for all μApps. 
    
    The function is activated once all μApps finish execution, that is, the μApp counter ``t`` reaches the expected count [number of currently operational 
    microservices] 

    The function constructs a string that incorporates the RT-E2 Policy Report, then sends this string over a ZeroMQ socket.

    Raises:
        zmq.ZMQError: Handles ZeroMQ errors such as a failed send operation, including retries if necessary.
    """
    global ran_index, curricid, string_to_send_weight, string_to_send_ul_blanking, t
    # function implementation...


def get_metrics():
    """
    Fetches and parses metrics data from RAN. It decodes the received messages
    and stores the data in a structured dictionary format per UE (User Equipment).

    The function blocks until data is received, processes the data to calculate
    the number of UEs, and parses each UE's data into a dictionary including
    parameters like CQI, SNR, backlog, pending data, and transmitted bytes.

    Returns:
        dict: A dictionary where each key is an RNTI (Radio Network Temporary Identifier)
              and each value is another dictionary containing metrics for that UE.
              
    Raises:
        zmq.ZMQError: An error occurred due to ZeroMQ issues, like no data being available.
        Exception: A general exception if something else goes wrong (e.g., decoding errors).
    """
    global ran_index, curricid, string_to_send_ul_blanking, string_to_send_weight
    # function implementation...


def send_control_μApp_i():
    """
    This function mainatins the message pertaining to a specific μApp. This message contains
    data for the actions to be taken for each UE, identified by their RNTIs. Once this function
    recieves the message from the corresponding μApp, it tells the edgeric agent about completion of
    the μApp execution for that TTI by incrementing a counter  ``t`` by 1.

    """
    global ran_index, curricid, string_to_send_ul_blanking, string_to_send_weight
    # function implementation...





#### This is an example of a Downlink RBG scheduling μApp
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import math
import time
from utils import *
import redis
from edgeric_messenger import *           #import edgeric agent

def compute_policy():
   flag = False # to be deleted
   ue_data = get_metrics()            #### subscribe to RAN via the RT-E2 agent to receive metrics
   numues = len(ue_data)
   weights = np.zeros(numues * 2)
   RNTIs = list(ue_data.keys())

   for i in range(numues):
      # Store RNTI and corresponding weight
      weights[i*2+0] = RNTIs[i]
      weights[i*2+1] = 1/numues

   send_control_μApp_1(weights,flag)   #### send the scheduling control action to the RT-E2 agent
   value_algo = "Fixed Weights"


if __name__ == "__main__":

   while True:
      compute_policy()