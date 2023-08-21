import os
import shutil
import subprocess

UPLOAD_FOLDER = os.path.abspath("models/dense_vnet_abdominal_ct/input")
OUTPUT_FOLDER = os.path.abspath("./models/dense_vnet_abdominal_ct/output")

DEBUG = 0

class Abdominal_model:

    def __init__(self, saved_path):
        # Generate necessary folders 
        self.config_path = saved_path
        if os.path.isdir(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
        os.mkdir(UPLOAD_FOLDER)
        if os.path.isdir(OUTPUT_FOLDER):
            shutil.rmtree(OUTPUT_FOLDER)
        os.mkdir(OUTPUT_FOLDER)


    def predict(self, file):

        # Move to the model directory
        os.chdir("models/dense_vnet_abdominal_ct")

        # Save the file to the input folder
        file.save(os.path.join("/usr/src/app/models/dense_vnet_abdominal_ct/input", "seg_CT.nii"))

        # Command to run the model  
        command = [
            'python3',
            '-m',
            'monai.bundle',
            'run',
            '--config_file',
            'configs/inference.json',
            '--datalist',
            "['input/seg_CT.nii']",
            '--output_dir',
            'output/'
        ]

        process = subprocess.Popen(command)
        process.wait() 
        
        # Output path for the segmentation
        output_path = "/usr/src/app/models/dense_vnet_abdominal_ct/output/seg_CT/seg_CT_trans.nii.gz"

        # Move back to the root directory
        os.chdir("../..")
        
        return output_path

    def cleanup(self):
        if os.path.isdir(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
        os.mkdir(UPLOAD_FOLDER)
        if os.path.isdir(OUTPUT_FOLDER):
            shutil.rmtree(OUTPUT_FOLDER)
        os.mkdir(OUTPUT_FOLDER)


SAVED_CONFIG_PATH = os.path.abspath("./models/dense_vnet_abdominal_ct/config.ini")
abdominal_model = Abdominal_model(SAVED_CONFIG_PATH)