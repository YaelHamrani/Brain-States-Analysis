# -*- coding: utf-8 -*-
"""
Created on Sun Oct 6 17:12:09 2024

@author: yaelh
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from preprocessing_tools import PrepTools
import os
import matplotlib.pyplot as plt
import shutil
import json

# Predefined values
ATLASES = {
    'AICHA': {'img': 'AICHA (Joliot 2015).nii', 'labels': 'AICHA (Joliot 2015).txt', 'yeo': 'AICHA-Yeo.xlsx'},
    'Schaefer2018_7Networks': {
        'img': 'Schaefer2018_400Parcels_7Networks_order_Tian_Subcortex_S4_3T_MNI152NLin2009cAsym_2mm.nii.gz',
        'labels': 'Schaefer2018_400Parcels_7Networks_order_Tian_Subcortex_S4_3T_MNI152NLin2009cAsym_2mm_label_modified.txt',
        'yeo': 'SchafferTian-Yeo.xlsx'},
    'Lausanne': {'img': 'atl-Cammoun2012_space-MNI152NLin2009aSym_res-250_deterministic.nii.gz',
                 'labels': 'Lausanne_463.txt', 'yeo': 'Lausanne_463.txt'}
}

YEO_NW = ['VIS', 'SOM', 'DAT', 'VAT', 'LIM', 'FPN', 'DMN']

CONFOUNDS_FULL = ['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z',
                  'a_comp_cor_00', 'a_comp_cor_01', 'a_comp_cor_02', 'a_comp_cor_03', 'a_comp_cor_04', 'a_comp_cor_05',
                  'csf', 'white_matter', 'framewise_displacement']

CONFOUNDS_BASIC = ['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z', 'framewise_displacement']


class ConfigGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test Configuration")
        self.geometry("600x700")

        # Track if run buttons are already shown
        self.run_buttons_shown = False

        # Configuration dictionary to hold the parameters
        self.config = {}

        # Choose between reading an existing config or creating a new one
        tk.Label(self, text="Choose Configuration Option").pack(pady=10)
        tk.Button(self, text="Read from Config File", command=self.read_config_file).pack(pady=5)
        tk.Button(self, text="Create New Config File", command=self.create_config_form).pack(pady=5)

        # Section to display when reading from config or creating new config
        self.frame = tk.Frame(self)
        self.frame.pack(pady=10)

        # Buttons to run scripts once configuration is loaded
        self.run_frame = tk.Frame(self)
        self.run_frame.pack(pady=10)

    def read_config_file(self):
        # Let user choose a config file
        config_file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not config_file_path:
            messagebox.showerror("Error", "Please select a valid config file.")
            return

        # Load the config parameters from the selected file
        with open(config_file_path, 'r') as file:
            self.config = json.load(file)
            messagebox.showinfo("Success", "Config loaded successfully.")

        # Show the loaded parameters in the form
        self.show_config_in_form()

        # Show buttons to run the scripts
        self.show_run_buttons()

    def show_config_in_form(self):
        # Destroy existing form elements in the frame if any
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Populate form fields with the loaded config
        tk.Label(self.frame, text="Loaded Configuration Parameters").pack(pady=5)

        self.data_entry = self.create_form_entry("Data/Test Name", self.config.get('data', 'ProjectName'))
        self.project_root_output = self.create_form_entry("Project Output Root",self.config.get('project_root_output', r'D:\fMRI_preprocess'))
        self.data_root = self.create_form_entry("Data Root", self.config.get('data_root', r'D:\fMRI_preprocess'))
        self.t_r_entry = self.create_form_entry("T_R", str(self.config.get('T_R', '0.8')))
        self.confounds_var = self.create_form_entry("Confounds",self.config.get('CONFOUNDS','BASIC'))
        self.atlas_var = self.create_form_entry("Atlas", self.config.get('ATLAS', 'Schaefer2018_7Networks'))


    def create_config_form(self):
        # Destroy existing form elements in the frame if any
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Create form for inputting configuration parameters
        tk.Label(self.frame, text="Enter Configuration Parameters").pack(pady=5)
        # Atlas Choice
        tk.Label(self.frame, text="Select Atlas").pack(pady=5)
        self.atlas_var = tk.StringVar(value=list(ATLASES.keys())[1])
        self.atlas_menu = tk.OptionMenu(self.frame, self.atlas_var, *ATLASES.keys())
        self.atlas_menu.pack()

        self.data_entry = self.create_form_entry("Data/Test Name", "ProjectName")
        self.project_root_output = self.create_form_entry("Project Output Root", r'D:\fMRI_preprocess')
        self.data_root = self.create_form_entry("Data Root", r'\\D:\fmriprep')
        self.t_r_entry = self.create_form_entry("T_R", "0.8")
        self.nifti_ext_entry = self.create_form_entry("NIFTI Extension", "gz")
        self.num_vol_remove_entry = self.create_form_entry("Number of Volumes to Remove", "3")
        self.level_entry = self.create_form_entry("Level", "2")
        self.atlas_path_entry = self.create_form_entry("Atlas Path", r'D:\fMRI_preprocess\atlas')
        self.nifti_name_include = self.create_form_entry("NIFTI_NAME_INCLUDE (comma separated)", 'rest,desc-preproc_bold.nii.gz')
        self.conf_name_include =  self.create_form_entry("Confounds Name to Include",'rest')

        # Confounds Choice (Basic or Full)
        tk.Label(self.frame, text="Select Confounds").pack(pady=5)
        self.confounds_var = tk.StringVar(value="BASIC")
        tk.Radiobutton(self.frame, text="BASIC", variable=self.confounds_var, value="BASIC").pack()
        tk.Radiobutton(self.frame, text="FULL", variable=self.confounds_var, value="FULL").pack()



        # Save Config Button
        tk.Button(self.frame, text="Save Config", command=self.save_new_config).pack(pady=10)

    def create_form_entry(self, label_text, default_value):
        tk.Label(self.frame, text=label_text).pack()
        entry = tk.Entry(self.frame)
        entry.insert(0, default_value)
        entry.pack(pady=5)
        return entry

    def save_new_config(self):
        # Collect input from the form and store it in the config dictionary
        self.config['data'] = self.data_entry.get()
        self.config['project_root_output'] = self.project_root_output.get()
        self.config['data_root'] = self.data_root.get()
        self.config['T_R'] = float(self.t_r_entry.get())
        self.config['NIFTI_EXT'] = self.nifti_ext_entry.get()
        self.config['NUM_VOL_TO_REMOVE'] = int(self.num_vol_remove_entry.get())
        self.config['LEVEL'] = int(self.level_entry.get())
        self.config['ATLAS'] = self.atlas_var.get()
        self.config['ATLAS_PATH'] = self.atlas_path_entry.get()
        self.config['NIFTI_NAME_INCLUDE'] = self.nifti_name_include.get()
        self.config['CONF_NAME_INCLUDE'] = self.conf_name_include.get()

        # Add confounds based on the choice
        if self.confounds_var.get() == "FULL":
            self.config['CONFOUNDS'] = CONFOUNDS_FULL
        else:
            self.config['CONFOUNDS'] = CONFOUNDS_BASIC

        # Add default parameters
        self.config['STANDARTIZE'] = 'zscore'
        self.config['SMOOTHING_FWHM'] = 6
        self.config['DETREND'] = True
        self.config['HIGH_PASS'] = 0.01
        self.config['LOW_PASS'] = 0.08
        self.config['DEBUG'] = False

        # Collect additional parameters
        self.config['changable_TR'] = False
        self.config['YEO_NW'] = YEO_NW
        self.config['RESULTS'] = os.path.join(self.config['project_root_output'], self.config['data'] + '_output','Results_' + self.config['ATLAS'])
        self.config['LOG'] = os.path.join(self.config['project_root_output'], self.config['data'] + '_output', 'log')
        # Ask user to save the config file
        save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if save_path:
            with open(save_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            messagebox.showinfo("Success", "Config file saved successfully.")

            # Show buttons to run the scripts
            self.show_run_buttons()
        else:
            messagebox.showerror("Error", "Failed to save config file.")

    def show_run_buttons(self):
        # Check if buttons are already shown
        if self.run_buttons_shown:
            return  # Don't create them again

        # Destroy existing buttons in the run frame if any
        for widget in self.run_frame.winfo_children():
            widget.destroy()

        # Create buttons to run scripts after config is loaded or created
        tk.Label(self.run_frame, text="Select Function to Run").pack(pady=10)
        tk.Button(self.run_frame, text="Run Preprocessing", command=self.run_preprocessing).pack(pady=5)
        # Button to trigger the "Remove Bad Scrabs" function
        tk.Button(self, text="Remove Bad Scrabs", command=self.open_scrabs_gui).pack(pady=10)
        # Update the flag to indicate buttons are shown
        self.run_buttons_shown = True

    def open_scrabs_gui(self):
        """Open the ScrabsGUI window for removing bad scrabs"""
        ScrabsGUI(self.config)

    def run_preprocessing(self):
        # Assuming `self.config` is your configuration dictionary
        prep_params = PrepParams(self.config)
        if not os.path.exists(prep_params.RESULTS):
            os.makedirs(prep_params.RESULTS)
        if not os.path.exists(prep_params.LOG):
            os.makedirs(prep_params.LOG)
        prep_params.LOG_FILE = os.path.join(prep_params.LOG, 'log_file.txt')

        prep_params.LOG_PARAM = os.path.join(prep_params.LOG, 'log_param.txt')
        sets_of_files, labels, atlas_img = PrepTools.LoadData(prep_params)


        for set_of_files_i in range(len(sets_of_files)):
            set_of_files = sets_of_files[set_of_files_i]

            # Generate the CSV file path
            output_csv_path = os.path.join(
                prep_params.RESULTS,
                set_of_files['NIFTI'].split('\\')[-1].split('.')[0] + '.csv'
            )

            # Check if the output CSV file already exists
            if os.path.exists(output_csv_path):
                print(f"File already exists. Skipping: {output_csv_path}")
                continue  # Skip processing this file

            # Step 1 - remove first NUM_VOL_TO_REMOVE volumes
            nifti_sliced = PrepTools.RemoveFirstNVolumes(nifti=set_of_files['NIFTI'],
                                                         num_vol_to_remove=prep_params.NUM_VOL_TO_REMOVE)

            conf_, continue_ = PrepTools.handleConf(set_of_files, prep_params)
            if continue_: continue
            if prep_params.changable_TR: prep_params.T_R = PrepTools.GetTR(set_of_files['NIFTI'])
            if prep_params.T_R is None: continue

            if prep_params.data == 'JOY_add':
                atlas_img = PrepTools.AddRois(st_atlas_img)

            # Create the time series from the fMRI data
            time_series = PrepTools.CreatTimeSeries(nifti_img=nifti_sliced, atlas=atlas_img, labels=labels,
                                                    standardize=prep_params.STANDARTIZE, smoothing_fwhm=prep_params.SMOOTHING_FWHM,
                                                    detrend=prep_params.DETREND,
                                                    low_pass=prep_params.LOW_PASS, high_pass=prep_params.HIGH_PASS, t_r=prep_params.T_R,
                                                    confounds=conf_)


            # Save the results
            df = pd.DataFrame(time_series)
            if not os.path.exists(prep_params.RESULTS):
                os.makedirs(prep_params.RESULTS)
            df.to_csv(output_csv_path, index=False)
            print(f"Saved: {output_csv_path}")


##################################################

class ScrabsGUI(tk.Toplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Remove Bad Scrabs")
        self.geometry("600x800")

        # Inherit configuration from the parent ConfigGUI
        self.config = config
        self.prep_params = PrepParams(config)


        # Default threshold value (can be modified by the user)
        self.threshold_value = tk.DoubleVar(value=0.15)

        # Section to display when reading from config or creating new config
        self.frame = tk.Frame(self)
        self.frame.pack(pady=10)

        # Buttons to run scripts once configuration is loaded
        self.run_frame = tk.Frame(self)
        self.run_frame.pack(pady=10)

        # Add threshold selection slider
        self.create_threshold_slider()

        # Button to trigger the "Visualize Bad Scrabs" function
        tk.Button(self, text="Visualize Bad Scrabs", command=self.visualize_bad_scrabs).pack(pady=10)

        # Button to trigger the removal after visualizing
        tk.Button(self, text="Remove Bad Scrabs", command=self.remove_bad_scrabs).pack(pady=10)

        # Variables to store data for scrabs
        self.bad_scrabs_percentages = []
        self.bad_scrabs_files = []
        self.file_list = []

    def create_threshold_slider(self):
        """Create a slider to adjust the threshold dynamically"""
        tk.Label(self, text="Adjust Threshold for Bad Scrabs Removal").pack(pady=10)
        slider = tk.Scale(self, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, variable=self.threshold_value)
        slider.pack(pady=10)



    def get_confound_files(self,log_file_path):
        # Read the log file (which is in JSON format)
        with open(log_file_path, 'r') as file:
            log_data = json.load(file)

        # Extract only the "CONFOUND" field from each entry
        confound_files = [entry['CONFOUND'] for entry in log_data if 'CONFOUND' in entry]

        return confound_files

    def get_common_prefix(self,filename, suffix):
        """Remove the specific suffix from the filename to extract the common part."""
        if filename.endswith(suffix):
            return filename.replace(suffix, '')
        return None

    def get_matching_files(self,logs_path, results_dir):
        # Define the suffix to remove from the files to get the common part
        suffixs = ['_desc-confounds_timeseries.txt', '_desc-confounds_regressors.txt'] # This can be adjusted if needed
        for suffix in suffixs:
            # Get list of files from each directory
            log_files = os.listdir(logs_path)
            # Filter files that end with the specified suffix
            filtered_log_files = [f for f in log_files if f.endswith(suffix)]
            log_file_path = os.path.join(logs_path, 'log_file.txt')
            conf_files = self.get_confound_files(log_file_path)
            results_files = os.listdir(results_dir)
            if len(filtered_log_files)>1:
                break
        # Dictionary to store the matching files
        matched_files = {}

        # Match based on common substring (e.g., sub-24001_task-rest1)
        for path_file in filtered_log_files:
            # Extract the common part from the path file
            common_id = self.get_common_prefix(path_file, suffix)

            if common_id:
                # Initialize a dictionary to store the matching pair for each set
                matched_files[common_id] = {}

                # Add the pathdir file
                matched_files[common_id]['LOG'] = os.path.join(logs_path, path_file)

                # Find matching log file
                matching_conf_file = next((f for f in conf_files if common_id in f), None)
                if matching_conf_file:
                    matched_files[common_id]['CONF'] = matching_conf_file

                # Find matching results file
                matching_results_file = next((f for f in results_files if common_id in f), None)
                if matching_results_file:
                    matched_files[common_id]['RESULTS'] = os.path.join(results_dir, matching_results_file)

        return matched_files

    def visualize_bad_scrabs(self):
        """Visualize the number of bad scrabs over the chosen threshold"""
        threshold = self.threshold_value.get()
        logs_path = self.prep_params.LOG
        results_dir = self.prep_params.RESULTS

        TSV = True

        # Perform the scrab detection and count
        self.bad_scrabs_percentages = []
        self.bad_scrabs_files = []
        self.file_list = []
        list_of_match_files = self.get_matching_files(logs_path, results_dir)

        if TSV:
            for sub in list_of_match_files:
                # Read the CONF file to get the number of rows (shape[0])
                file_item = list_of_match_files[sub]
                try:
                    conf_df = pd.read_csv(file_item['CONF'], sep='\t')  # Assuming TSV
                    total_rows = conf_df.shape[0]
                except Exception as e:
                    print(f"Error reading CONF file: {file_item['CONF']}, {str(e)}")
                    continue

                # Read the LOG file and find lines that match 'FD_motion_outlier'
                try:
                    with open(file_item['LOG'], 'r') as log_file:
                        lines = log_file.readlines()
                    indices = [index for index, line in enumerate(lines) if 'FD_motion_outlier' in line]
                except Exception as e:
                    print(f"Error reading LOG file: {file_item['LOG']}, {str(e)}")
                    continue

                # Calculate the percentage of bad scrabs
                percentage = (len(indices) / total_rows) * 100
                # Append the results to the lists for visualization
                self.file_list.append(file_item['CONF'])  # Add CONF file for reference in visualization
                self.bad_scrabs_percentages.append(percentage)
                # If percentage exceeds the threshold, append the RESULTS file
                if percentage > threshold * 100:
                    self.bad_scrabs_files.append(file_item['RESULTS'])
        # Visualize the percentage of bad scrabs
        self.show_visualization(threshold)





    def show_visualization(self, threshold):
        """Visualize the number of bad scrabs and show the user"""
        plt.figure(figsize=(10, 5))
        plt.barh(self.file_list, self.bad_scrabs_percentages, color='red')
        plt.axvline(x=threshold * 100, color='blue', linestyle='--', label=f"Threshold: {threshold * 100}%")
        plt.xlabel("Percentage of Bad Scrabs (%)")
        plt.ylabel("File")
        plt.title("Percentage of Bad Scrabs in Each File")
        plt.legend()
        plt.tight_layout()
        plt.show()

    def remove_bad_scrabs(self):
        """Move bad scrab files to a subfolder if over threshold"""
        threshold = self.threshold_value.get()

        # Ensure the visualization was done first
        if not self.file_list:
            messagebox.showerror("Error", "Please visualize bad scrabs before removing.")
            return

        results_dir = self.prep_params.RESULTS

        # Create a subfolder for bad scrabs
        bad_scrabs_folder = os.path.join(results_dir, "bad_scrabs")

        # Create the folder if it doesn't exist
        if not os.path.exists(bad_scrabs_folder):
            os.makedirs(bad_scrabs_folder)

        # Move files that exceed the threshold to the bad scrabs folder
        for file in self.bad_scrabs_files:
            file_name = os.path.basename(file)
            destination = os.path.join(bad_scrabs_folder, file_name)
            shutil.move(file, destination)

        messagebox.showinfo("Success", f"Moved {len(self.bad_scrabs_files)} files to 'bad scrabs' folder.")


class PrepParams:
    def __init__(self, config):
        # Initialize all the parameters from the config dictionary
        self.data = config.get('data')
        self.ATLAS_PATH = config.get('ATLAS_PATH')
        self.atlas = config.get('ATLAS')
        self.project_root = config.get('data_root')
        self.STANDARTIZE = config.get('STANDARTIZE')
        self.SMOOTHING_FWHM = config.get('SMOOTHING_FWHM')
        self.DETREND = config.get('DETREND')
        self.LOW_PASS = config.get('LOW_PASS')
        self.HIGH_PASS = config.get('HIGH_PASS')
        self.T_R = config.get('T_R')
        self.NUM_VOL_TO_REMOVE = config.get('NUM_VOL_TO_REMOVE')
        self.DEBUG = config.get('DEBUG')
        self.RESULTS = config.get('RESULTS')
        self.LOG = config.get('LOG')
        self.changable_TR = config.get('changable_TR')
        self.LEVEL = config.get('LEVEL')
        self.NIFTI_EXT = config.get('NIFTI_EXT')
        self.NIFTI_NAME_INCLUDE = config.get('NIFTI_NAME_INCLUDE').split(',')
        self.CONF_NAME_INCLUDE = config.get('CONF_NAME_INCLUDE').split(',')
        self.data_root = self.project_root
        self.CONF_EXT = 'tsv'
        self.NIFTI_NAME_EXCLUDE = []
        self.CONF_NAME_EXCLUDE = []
        self.MATCHING_TEMPLATE = ['sub-', '_space']
        self.WITHIN_BETWEEN = os.path.join(self.RESULTS, 'withinbetween.xlsx')
        self.INCLUDE_MOTION_CONF = True
        self.ATLAS_IMG_PATH = os.path.join(self.ATLAS_PATH, ATLASES[self.atlas]['img'])
        self.ATLAS_LABELS_PATH = os.path.join(self.ATLAS_PATH, ATLASES[self.atlas]['labels'])
        self.AICHA_YEO_PATH = os.path.join(self.ATLAS_PATH, ATLASES[self.atlas]['yeo'])
        self.CONFOUNDS = config.get('CONFOUNDS')

    def display_params(self):
        # A method to display the current parameters (optional)
        for key, value in self.__dict__.items():
            print(f"{key}: {value}")


# Create and start the GUI
if __name__ == "__main__":
    app = ConfigGUI()
    app.mainloop()





