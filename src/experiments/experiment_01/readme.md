# Getting Started
## Running Simulation and Saving Reports
Navigate to this experiment's directory in your terminal and run the following command:

$ ```python3 main.py [--flag]```

Leave `[--flag]` empty to open a GUI for the simulation. This will slow down the simulation significantly and requires you to click the **play** button to start the simulation.
Or, type `--nogui` to run the simulation without a GUI.

Once the simulation begins to run, the terminal will display the message *"Running simulation. Please wait..."* This may take a few minutes.

Once the simulation has finished, you'll see the message *"Simulation over."* during which time the runner script will process, package, and save all relevant data into separate files.

Each exported file will be displayed to you. For example:


  - *"Saved results to: **reports/laneVolumes_20211114_13-49-28.csv**"*
  - *"Saved results to: **reports/edgeInfo_20211114_13-49-28.csv**"*
  - ... and so on.

# Data Processing
SUMO exports various metrics throughout each simulation in XML format. These files can be massive in size. However, not all the data is relevent for our needs. After each simulation ends, we process and package the relevent data into timestamped CSV files. 

To preserve memory, the XML files are overwritten with each new simulation run. For this reason, we prefix each of these files with the word "temp" to help distinguish them from permenant report files.