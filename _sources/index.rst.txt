.. Edge_RIX documentation master file, created by
   sphinx-quickstart on Mon Nov 20 16:41:50 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

EdgeRIC: Delivering Real-time Intelligence to Radio Access Networks
========================================================================

.. image:: edgeric-intro.png
  :width: 700
  :alt: sample text

.. NextG cellular networks must support a wide variety of applications that require radio access with latency, 
.. throughput and reliability guarantees hitherto unavailable. Simultaneously, the environment is becoming in-
.. creasingly dynamic over diverse spectrum bands, user mobility patterns and variable traffic patterns. Com-
.. plex cross layer interactions imply that problems without crisp models are emerging where a data-driven 
.. machine learning approach to optimal resource utilization has value. We introduce EdgeRIC, a real-time RIC 
.. co-located with the Distributed Unit (DU). It is decoupled from the RAN stack, and operates at the RAN timescale.

- EdgeRIC is a platform for **real-time AI-in-the-loop** for decision and control in cellular networks. It is designed to access network and application-level information to execute AI-optimized and other policies in real-time (sub-millisecond) .



.. .. raw:: html

..    <div class="side-by-side">
..      <div class="video">
..        <video width="500" height="380" controls>
..          <source src="_static/beamarmor_demo.mp4" type="video/mp4" controls autoplay>
..          Your browser does not support the video tag.
..        </video>
..      </div>
..       <div class="video">
..        <video width="500" height="380" controls>
..          <source src="_static/demo-2.mp4" type="video/mp4" controls autoplay>
..          Your browser does not support the video tag.
..        </video>
..      </div>
..    </div>

.. EdgeRIC Focus Areas
.. ------------------------

.. .. image:: edgeric-focus.png
..   :width: 600
..   :alt: sample text



Our Projects
------------------------

.. raw:: html

   <div class="project-grid">
     <a href="projects/cloud-gaming.html" class="project-card" id="card-cloud-gaming">
       <h3>Cloud Gaming on 5G</h3>
     </a>
     <a href="projects/multimodal-sensing.html" class="project-card" id="card-multimodal">
       <h3>mmsRAN: MultiModal Sensing</h3>
     </a>
     <a href="projects/telemetry.html" class="project-card" id="card-telemetry">
       <h3>SCOUT: Telemetry with a Packet Centric Lens</h3>
     </a>
     <a href="projects/qoe-networking.html" class="project-card" id="card-qoe">
       <h3>QoE-aware Networking</h3>
     </a>
     <a href="projects/other-muapps.html" class="project-card" id="card-muapps">
       <h3>Other μApps</h3>
     </a>
     <a href="projects/tiny-twin.html" class="project-card" id="card-tiny-twin">
       <h3>Tiny-twin</h3>
     </a>
   </div>

.. toctree::
   :maxdepth: 1
   :caption: Our Projects
   :hidden:

   projects/cloud-gaming
   projects/multimodal-sensing
   projects/telemetry
   projects/qoe-networking
   projects/other-muapps
   projects/tiny-twin


Our Team
------------------------

.. raw:: html

   <div class="team-grid">
     <div class="team-card">
       <div class="team-photo" id="photo-dinesh"></div>
       <h4>Dinesh Bharadia</h4>
       <p>Professor, UCSD</p>
       <a href="mailto:dineshb@ucsd.edu" class="team-email">dineshb@ucsd.edu</a>
     </div>
     <div class="team-card">
       <div class="team-photo" id="photo-srinivas"></div>
       <h4>Srinivas Shakkottai</h4>
       <p>Professor, TAMU</p>
       <a href="mailto:sshakkot@tamu.edu" class="team-email">sshakkot@tamu.edu</a>
     </div>
     <div class="team-card">
       <div class="team-photo" id="photo-ish"></div>
       <h4>Ish Jain</h4>
       <p>Professor, RPI</p>
       <a href="mailto:jaini2@rpi.edu" class="team-email">jaini2@rpi.edu</a>
     </div>
     <div class="team-card">
       <div class="team-photo" id="photo-ushasi"></div>
       <h4>Ushasi Ghosh</h4>
       <p>PhD Student, UCSD</p>
       <a href="mailto:ughosh@ucsd.edu" class="team-email">ughosh@ucsd.edu</a>
     </div>
     <div class="team-card">
       <div class="team-photo" id="photo-sushila"></div>
       <h4>Sushila Seshasayee</h4>
       <p>PhD Student, UCSD</p>
       <a href="mailto:sseshasa@ucsd.edu" class="team-email">sseshasa@ucsd.edu</a>
     </div>
     <div class="team-card">
       <div class="team-photo" id="photo-Ali"></div>
       <h4>Ali Mamaghani</h4>
       <p>PhD Student, UCSD</p>
       <a href="mailto:amamaghani@ucsd.edu" class="team-email">amamaghani@ucsd.edu</a>
     </div>
     <div class="team-card">
       <div class="team-photo" id="photo-qingyuan"></div>
       <h4>Qingyuan Zheng</h4>
       <p>MS Student, UCSD</p>
       <a href="mailto:qiz066@ucsd.edu" class="team-email">qiz151@ucsd.edu</a>
     </div>
     <div class="team-card">
       <div class="team-photo" id="photo-Woo"></div>
       <h4>Woo Hyun Ko</h4>
       <p>Senior Research Engineer, TAMU</p>
       <a href="mailto:whko@tamu.edu" class="team-email">whko@tamu.edu</a>
     </div>
   </div>


Demos 
------------------------

.. raw:: html

   <div class="video-grid">
     <div class="video-card">
       <div class="video-card-content">
         <h3>BeamArmor</h3>
         <p>Anti-jamming: Controlling MIMO weights in realtime to steer the beam null toward the jammer</p>
       </div>
       <div class="video-wrapper">
         <div class="video-cover" data-poster="demo_figs/beamarmor_cover.jpg">
           <button type="button" class="video-play-btn" aria-label="Play video"></button>
         </div>
         <video preload="metadata" data-src="_static/beamarmor_demo.mp4">
           Your browser does not support the video tag.
         </video>
       </div>
     </div>
     <div class="video-card">
       <div class="video-card-content">
         <h3>AI Scheduling</h3>
         <p>RL-based scheduling policy trained to maximize overall system throughput</p>
       </div>
       <div class="video-wrapper">
         <div class="video-cover" data-poster="demo_figs/demo2_cover.jpg">
           <button type="button" class="video-play-btn" aria-label="Play video"></button>
         </div>
         <video preload="metadata" data-src="_static/demo-2.mp4">
           Your browser does not support the video tag.
         </video>
       </div>
     </div>
     <div class="video-card">
       <div class="video-card-content">
         <h3>Multi-site Management</h3>
         <p>Interference-aware resource distribution across sites with Near-RT RIC</p>
       </div>
       <div class="video-wrapper">
         <div class="video-cover" data-poster="demo_figs/sparc_cover.jpg">
           <button type="button" class="video-play-btn" aria-label="Play video"></button>
         </div>
         <video preload="metadata" data-src="_static/sparc-video-demo.mov">
           Your browser does not support the video tag.
         </video>
       </div>
     </div>
   </div>

EdgeRIC Events
------------------------

.. toctree::
   :maxdepth: 2
   :caption: EdgeRIC Events
   :hidden:

   oaic-workshop-2024.rst
   srsran-2024-workshop.rst

.. raw:: html

   <div class="event-list">
     <a class="event-card" href="oaic-workshop-2024.html">
       <div class="event-date">2024</div>
       <div class="event-main">
         <div class="event-title">OAIC Workshop 2024</div>
         <div class="event-desc">Tutorials, demos, and hands-on sessions for OAI + EdgeRIC.</div>
       </div>
       <div class="event-cta">View</div>
     </a>
     <a class="event-card" href="srsran-2024-workshop.html">
       <div class="event-date">2024</div>
       <div class="event-main">
         <div class="event-title">srsRAN Workshop 2024</div>
         <div class="event-desc">EdgeRIC integration, experiments, and live testbed walkthroughs.</div>
       </div>
       <div class="event-cta">View</div>
     </a>
   </div>

Open Source Repositories
------------------------

.. raw:: html

   <div class="repo-list">
     <div class="repo-card">
       <h3>srsRAN-4G + EdgeRIC</h3>
       <p class="repo-meta"><strong>Release Date:</strong> TBD</p>
       <p><strong>Description:</strong> EdgeRIC integrated with srsRAN 4G</p>
       <a href="#" class="repo-link" target="_blank" rel="noopener noreferrer">View on GitHub</a>
     </div>
     <div class="repo-card">
       <h3>srsRAN-5G (2024) + EdgeRIC</h3>
       <p class="repo-meta"><strong>Release Date:</strong> 2024</p>
       <p><strong>Description:</strong> EdgeRIC on srsRAN 5G 2024 release</p>
       <a href="https://github.com/ucsdwcsng/EdgeRIC-on-5G/tree/srsran" class="repo-link" target="_blank" rel="noopener noreferrer">View on GitHub</a>
     </div>
     <div class="repo-card">
       <h3>srsRAN-5G (25.10) + EdgeRIC</h3>
       <p class="repo-meta"><strong>Release Date:</strong> 25.10</p>
       <p><strong>Description:</strong> EdgeRIC on srsRAN 5G 25.10 release</p>
       <a href="#" class="repo-link" target="_blank" rel="noopener noreferrer">View on GitHub</a>
     </div>
     <div class="repo-card">
       <h3>OAI + EdgeRIC</h3>
       <p class="repo-meta"><strong>Release Date:</strong> Oct 01, 2025</p>
       <p><strong>Description:</strong> EdgeRIC integrated with OpenAirInterface</p>
       <a href="https://github.com/ucsdwcsng/EdgeRIC-5G-OAI" class="repo-link" target="_blank" rel="noopener noreferrer">View on GitHub</a>
     </div>
   </div>








5G Testbed
------------------------

.. raw:: html

   <a href="5g-testbed.html">
     <img src="_static/5G-testbed.png" alt="5G Testbed" style="width: 700px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); cursor: pointer; transition: transform 0.2s ease;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
   </a>




.. Current Status
.. ------------------------

.. We are currently supported on the **srsRAN and OAI Projects**. 

.. .. image:: edgeric-architecture-overview.png
..   :width: 600
..   :alt: sample text


.. **Our Currently Supported Real time Metrics:**

.. .. image:: current-metrics.png
..   :width: 600
..   :alt: sample text

.. **Our Currently Supported Control Capabilities:**

.. .. image:: current-capabilities.png
..   :width: 600
..   :alt: sample text

.. **Refer to our 5G srsRAN version:** `Github (srsRAN) <https://github.com/ucsdwcsng/EdgeRIC-on-5G.git>`_  - Multi container solution available

.. **Refer to our 5G OAI version:** `Github (OAI) <https://github.com/ucsdwcsng/EdgeRIC-5G-OAI.git>`_  


.. Current Publications
.. ------------------------

.. .. tabs::

..     .. tab:: EdgeRIC 
..         Empowering Real-time Intelligent Optimization and Control in NextG Cellular Networks
        
..         **Paper**: `EdgeRIC <https://www.usenix.org/conference/nsdi24/presentation/ko>`_  
        
..         **Code**: `Github Respository <https://github.com/ushasigh/EdgeRIC-A-real-time-RIC.git>`_ 
        
..         **Website**: https://wcsng.ucsd.edu/edgeric/ 

..     .. tab:: BeamArmor
..         Seamless Anti-Jamming in 5G Cellular Networks with MIMO Null-steering

..         **Paper** `BamArmor <https://dl.acm.org/doi/10.1145/3638550.3641138>`_

..         **Code**: `Github Respository <https://github.com/ucsdwcsng/beamarmor.git>`_

..     .. tab:: Tiny-twin
..         A Lightweight and Verifiable Digital Twin for NextG Cellular Networks

..         **Paper**: `Tiny-twin <https://dl.acm.org/doi/abs/10.1145/3638550.3643625>`_

..     .. tab:: Windex
..         Realtime Neural Whittle Indexing for Scalable Service Guarantees in NextG Cellular Networks

..         **Paper**: `Windex <https://arxiv.org/abs/2406.01888>`_

..         **Code**: `Github Repository <https://github.com/ucsdwcsng/EdgeRIC_whittleIndex.git>`_

..     .. tab:: SPARC
..         SPARC: Spatio-Temporal Adaptive Resource Control for Multi-site Spectrum Management in NextG Cellular Networks  
        
..         **Paper**: `SPARC <https://dl.acm.org/doi/abs/10.1145/3696405>`_ 

..         **Code**: `Github Respository <https://github.com/ushasigh/SPARC-multi-siteManagent.git>`_ 

..         **Website**: https://wcsng.ucsd.edu/sparc/ 

.. toctree::
   :maxdepth: 1
   :caption: 5G Testbed
   :hidden:

   5g-Testbed



EdgeRIC Architecture
------------------------

.. toctree::
   :maxdepth: 2
   :hidden:

   edgeric-architecture.rst

.. raw:: html

   <div class="arch-section-list">
     <a class="arch-section" href="edgeric-architecture.html">
       <div class="arch-section-title">RT-E2 interface (Real time E2 interface)</div>
       <div class="arch-section-desc">Messaging framework between the RAN stack and EdgeRIC, built on ZMQ and protobuf, with TTI-level synchronization.</div>
     </a>
     <a class="arch-section" href="edgeric-architecture.html">
       <div class="arch-section-title">RT-E2 Report Message</div>
       <div class="arch-section-desc">Per-UE KPI report structure (cqi, buffers, TBS, rates) sent every TTI from the RAN to EdgeRIC.</div>
     </a>
     <a class="arch-section" href="edgeric-architecture.html">
       <div class="arch-section-title">RT-E2 Policy Message</div>
       <div class="arch-section-desc">Control-action messages from μApps back to the RAN, including scheduling weights and blanking decisions.</div>
     </a>
     <a class="arch-section" href="edgeric-architecture.html">
       <div class="arch-section-title">REDIS database</div>
       <div class="arch-section-desc">How Redis is used for model storage, μApp lifecycle management, and dynamic configuration.</div>
     </a>
     <a class="arch-section" href="edgeric-architecture.html">
       <div class="arch-section-title">μApps – EdgeRIC microservices</div>
       <div class="arch-section-desc">How μApps subscribe to metrics, compute policies, and send control via the EdgeRIC messenger.</div>
     </a>
   </div>

EdgeRIC Tutorials
------------------------

.. toctree::
   :maxdepth: 2

   tutorials.rst

Datasets
------------------------

.. toctree::
   :maxdepth: 2

   datasets.rst

.. Research Papers
.. ------------------------
.. - EdgeRIC main paper: https://www.usenix.org/conference/nsdi24/presentation/ko
.. - BeamArmor: https://dl.acm.org/doi/10.1145/3638550.3641138
.. - Windex: https://arxiv.org/abs/2406.01888
.. - Tiny-twin: https://dl.acm.org/doi/abs/10.1145/3638550.3643625


.. Indices and tables
.. ==================

.. .. * :ref:`genindex`
.. .. * :ref:`modindex`
.. .. * :ref:`search`
.. toctree::
   :maxdepth: 2
   :hidden:

   gettingstarted.rst

Funding 
------------------------ 
This work was funded primarily by NSF Grants CNS 2312978, CNS 2312979 and in part by CNS 1955696, ECCS 2030245, ARO grant W911NF- 19-1-0367.
