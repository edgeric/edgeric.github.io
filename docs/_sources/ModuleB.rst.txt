
RT-E2 Report Message
--------------------
The RT-E2 report message includes per-UE key performance indicators (KPIs) received from the RAN. Each UE is identified by its unique RNTI (Radio Network Temporary Identifier) along with its corresponding KPIs.

Structure of the message:
``ue_data`` followed by ``RIC ID`` and ``RAN ID``.

**Message Details**:

- **ue_data**: Dictionary containing per-UE metrics. Each entry is keyed by the RNTI of the UE and contains the following KPIs:

  - ``CQI``: Channel Quality Indicator, reflecting the downlink channel quality.
  - ``BL``: Amount of backlog data waiting to be sent to the UE in the downlink.
  - ``SNR``: Signal-to-Noise Ratio in the uplink, indicating the quality of the uplink signal.
  - ``Pending_Data``: Data that is waiting to be sent in the uplink.
  - ``Tx``: The current downlinnk bitrate for the UE.

- **RIC ID**: This is the RIC index
- **RAN ID**: This is the RAN index or the TTI counter

**Example Data Structure**:

.. code-block:: python

    ue_data = {
        1001: {  # Example RNTI
            'CQI': 15, # Downlink Channel Quality Indicator
            'BL': 500,  # Downlink Backlog Buffer in Bytes
            'SNR': 20.5,  # Uplink SNR in dB
            'pending_data': 250,  # Uplink Pending Data in Bytes
            'Tx': 100  # Downlink bitrate in Mbps
        }
    }
    RIC_ID = 1
    RAN_ID = 101

This structured message is critical for performance management and optimization of network resources in real-time applications.


RT-E2 Policy Message
---------------

Structure of the message:
``μApp1-control-message``, ``μApp2-control-message`` followed by ``RIC ID`` and ``RAN ID``.  

Control message format:
    to support downlink scheduling:
    to support uplink RB blanking: