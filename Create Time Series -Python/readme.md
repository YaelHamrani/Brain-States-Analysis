# Brain State Analysis Pipeline GUI

This folder contains scripts and resources for analyzing brain states using preprocessed fMRI NIfTI files. The pipeline is encapsulated in a GUI that guides users through configuration, preprocessing, and visualization of brain state data.

# File Structure:
* main_gui.py
   * The main script that launches the GUI for the pipeline. It integrates the entire workflow, including configuration, preprocessing, and visualization.
* data_manager.py
   * Handles data loading, saving, and organization. Originally written by T. Marko and modified by Yael H.
* preprocessing_tools.py
   * Provides functions for extracting time series from fMRI data using atlas assignments and handling preprocessing tasks. Originally written by T. Marko and modified by Yael H.
* atlas/
   * A folder containing atlas files supported by the pipeline.
* config/
   * A folder containing example JSON configuration files for projects.

# Pipeline Overview:
## GUI Features:
### 1. Configuration Management
   * Create or load a configuration file containing project details:
        * Data path
        * Output directory
        * Project name
        * Atlas selection
        * NIfTI file extensions (.nii or .gz).
          
      ![image](https://github.com/user-attachments/assets/ddb75223-5707-4624-8b81-ce61d5f7297f)
           fig.1 Create New Config File at the bottom save the file as json file
     
### 2. Data Preprocessing
   * Extract time series for each fMRI file using atlas-based parcellation.
   *  Save results as CSV files where:
       * Rows correspond to TRs (time points).
       * Columns correspond to voxels in the atlas.
         
### 3. Data Visualization and Scrubbing
* Visualize extracted time series and inspect confounds (e.g., head movement).
Remove files with high percentages (15-22%) of bad scrubbing due to excessive motion.

# How to Use:
   ## 1. Run the GUI:
   python main_gui.py
   
   ![image](https://github.com/user-attachments/assets/0d6ab138-745c-402a-98ed-4f9dffe6ecf2)
              
               fig 2. Read from config file or creat new file for new project
               
   ## 2. Set Up Project:
   * Use the GUI to create or load a configuration file with all project details.
     
   ![image](https://github.com/user-attachments/assets/60c1e6ba-2ce5-4b4d-b6c1-7d51054057a9)

            fig 3. After reading config file the " Run Preprocessing " button appears

   ## 3. Preprocess Data:
   * Load fMRI data.
   * Extract time series using the selected atlas and save as CSV.

   ## 4. Scrub and Visualize:
   * Visualize confounds (e.g., head motion).
   * Remove datasets with >15-22% motion-related confounds.
    
   ## 5. Output:
   * Preprocessed data and time series saved to the output directory.
 
# Requirements:
* Python 3.7+
* Required libraries:
  * os
  * glob
  * numpy
  * pandas
  * matplotlib.pyplot
  * shutil
  * json
  * nibabel
  * nilearn
  * nipype.interfaces
  * nilearn.maskers 
  * scikit-learn
  * tkinter

Install dependencies using:
pip install -r requirements.txt

# Notes:
* The preprocessing assumes preprocessed NIfTI files are in .nii or .gz format.
* Example configuration files in config_examples/ can be used as templates.
* Supported atlases are provided in the supported_atlases/ folder.

# Contributors:
* T. Marko: Original implementation of data_manager.py and preprocessing_tools.py.
* Yael H.: Modifications and enhancements to data_manager.py and preprocessing_tools.py.
* Main GUI: Encapsulates the pipeline for seamless project management.

For questions or issues, please contact the maintainers or open an issue.
