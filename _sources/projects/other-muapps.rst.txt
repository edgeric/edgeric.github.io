Other μApps
===========

Overview
--------

EdgeRIC's μApp framework enables rapid development and deployment of custom network control applications. This page showcases additional μApps developed by our team and community.

.. note::
   Interested in building your own μApp? Check out our :doc:`/tutorials` guide.

Featured μApps
--------------

EdgeRIC
^^^^^^^
The core real-time RIC platform that enables sub-millisecond AI-in-the-loop control for cellular networks. EdgeRIC provides the foundation for all other μApps.

:doc:`Learn more about EdgeRIC </edgeric>` | **Paper**: `NSDI'24 <https://www.usenix.org/conference/nsdi24/presentation/ko>`_

BeamArmor
^^^^^^^^^
Anti-jamming μApp that controls MIMO beamforming weights in real-time to steer beam nulls toward jammers, protecting legitimate communications.

:doc:`Learn more about BeamArmor </beamarmor>` | **Paper**: `MobiCom'24 <https://dl.acm.org/doi/10.1145/3638550.3641138>`_

Windex
^^^^^^
Wireless inference and decision-making μApp for intelligent resource allocation based on learned network patterns.

:doc:`Learn more about Windex </windex>` | **Paper**: `arXiv <https://arxiv.org/abs/2406.01888>`_

SPARC
^^^^^
Multi-site coordination μApp enabling interference-aware resource distribution across multiple base stations through Near-RT RIC integration.

:doc:`Learn more about SPARC </sparc>` | **Paper**: Coming soon

.. Additional μApps
.. ----------------

.. Spectrum Sensing μApp
.. ^^^^^^^^^^^^^^^^^^^^^
.. Detects spectrum occupancy and interference patterns for dynamic spectrum access.

.. Energy Efficiency μApp
.. ^^^^^^^^^^^^^^^^^^^^^^
.. Optimizes power consumption while maintaining QoS requirements.

.. Mobility Prediction μApp
.. ^^^^^^^^^^^^^^^^^^^^^^^^
.. Predicts user movement patterns for proactive handover optimization.

.. Traffic Classification μApp
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. Real-time classification of application traffic for differentiated service.

.. Anomaly Detection μApp
.. ^^^^^^^^^^^^^^^^^^^^^^
.. Identifies unusual network behavior and potential security threats.

.. Building Custom μApps
.. ---------------------

.. The EdgeRIC μApp SDK provides:

.. 1. **Metrics API**: Access real-time RAN telemetry
.. 2. **Control API**: Send scheduling and configuration decisions
.. 3. **ML Integration**: Deploy trained models for inference
.. 4. **Testing Framework**: Validate μApps before deployment

Example μApp Template
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from edgeric_messenger import EdgeRICAgent

   class MyMuApp:
       def __init__(self):
           self.agent = EdgeRICAgent()
       
       def on_metrics(self, metrics):
           # Process incoming metrics
           decision = self.compute_policy(metrics)
           self.agent.send_control(decision)
       
       def compute_policy(self, metrics):
           # Your custom logic here
           pass

Community Contributions
-----------------------

We welcome μApp contributions from the research community. Contact us to have your μApp featured here.

Related Resources
-----------------

- :doc:`/edgeric-architecture`
- :doc:`/tutorials`
