Brain State Analysis Pipeline GUI
This folder contains scripts and resources for analyzing brain states using preprocessed fMRI NIfTI files. The pipeline is encapsulated in a GUI that guides users through configuration, preprocessing, and visualization of brain state data.

File Structure:
main_gui.py

The main script that launches the GUI for the pipeline. It integrates the entire workflow, including configuration, preprocessing, and visualization.
data_manager.py

Handles data loading, saving, and organization. Originally written by T. Marko and modified by Yael H.
preprocessing_tools.py

Provides functions for extracting time series from fMRI data using atlas assignments and handling preprocessing tasks. Originally written by T. Marko and modified by Yael H.
supported_atlases/

A folder containing atlas files supported by the pipeline.
config_examples/

A folder containing example JSON configuration files for projects.
Pipeline Overview:
GUI Features:
Configuration Management

Create or load a configuration file containing project details:
Data path
Output directory
Project name
Atlas selection
NIfTI file extensions (.nii or .gz).
Data Preprocessing

Extract time series for each fMRI file using atlas-based parcellation.
Save results as CSV files where:
Rows correspond to TRs (time points).
Columns correspond to voxels in the atlas.
Data Visualization and Scrubbing

Visualize extracted time series and inspect confounds (e.g., head movement).
Remove files with high percentages (15-22%) of bad scrubbing due to excessive motion.
How to Use:
Run the GUI:

bash
Copy code
python main_gui.py
Set Up Project:

Use the GUI to create or load a configuration file with all project details.
Preprocess Data:

Load fMRI data.
Extract time series using the selected atlas and save as CSV.
Scrub and Visualize:

Visualize confounds (e.g., head motion).
Remove datasets with >15-22% motion-related confounds.
Output:

Preprocessed data and time series saved to the output directory.
Requirements:
Python 3.7+
Required libraries:
numpy
pandas
matplotlib
nibabel
scikit-learn
PyQt5 or tkinter
Install dependencies using:

bash
Copy code
pip install -r requirements.txt
Notes:
The preprocessing assumes preprocessed NIfTI files are in .nii or .gz format.
Example configuration files in config_examples/ can be used as templates.
Supported atlases are provided in the supported_atlases/ folder.
Contributors:
T. Marko: Original implementation of data_manager.py and preprocessing_tools.py.
Yael H.: Modifications and enhancements to data_manager.py and preprocessing_tools.py.
Main GUI: Encapsulates the pipeline for seamless project management.
For questions or issues, please contact the maintainers or open an issue.
