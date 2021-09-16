# MELD project –  meld_focal_epilepsy

 `meld_focal_epilepsy`  – convert MELD dataset into a BIDS structure and send to the MELD team. 

## Overview
This program performs three steps :
 1. DICOMS TO NIFTI : Goes over the meld_template folder and convert DICOMs into NIFTI. Results save as nifti format (.nii). 
 2. NIFTI TO BIDS : Data are copied over a temporary folder and defaced. Data are converted into BIDS format using dcm2bids.
 3. COMPRESSION : BIDS folder is compressed and send over to the MELD team.

  
## Getting Started

### Prerequisites
This program requires the following softwares and libraries : 
- FSL 6.0
- Anaconda


### Installation
- [ ] Open a terminal and paste the following sentence : git clone https://github.com/mathrip/meld_focal_epilepsy.git
Press enter. Your package will be installed. 
- [ ] Install FSL : ADD LINK TO INSTRUCTIONS
- [ ] Install Anaconda: Add link to instructions
- [ ] Open a new terminal \
- [ ] ##ADD instructions for creating environment
Your meld_focal_epilepsy package is ready to be used. 

## Usage
1) Prepare the MELD data :\
    a. Copy the meld_template folder and rename with the MELD participant ID \
    b. Fill the folders with DICOMS/NIFTI from the respective sequences available (e.g T1w sequence acquired at 3T should go into the MELD_participantID/3T/T1/ folder)
2) Convert DICOMs into NIFTI. To launch the script, run \
python meld_bidsify_data_step1.py -d <participants_directory>
3) Create the lesion mask from the NIFTI T1 volume if not already done. Save the lesion mask as NIFTI into the right folder.
5) Convert NIFTI into BIDS format for the participants you which to send over. To launch the script, run \
python meld_bidsify_data_step1.py -d <participants_directory> -ids <list_participants> [optional arguments]

where : 
  - <meld_folder> : the path to the "meld_focal_epilepsy" directory.
  - <list_participants> : the path to the csv file containing the list of participant's ids you wish to share with the MELD team
  - optional arguments:
    - --nodeface : use this flag if you do not need to deface your NIFTI images.
    - --nodel (optional) : use this flag if you do not want to the temporary folder to be deleted 

Examples :
#Activate Anaconda environment
- conda activate mfe_env
#Run meld_bidsify scripts
- python meld_bidsify_data_step1.py -d /home/documents/meld_focal_epilepsy/
#Then create lesion masks
- python meld_bidsify_data_step2.py -d /home/documents/meld_focal_epilepsy/ -ids /home/documents/meld_focal_epilepsy/participants/list_participants_batch.csv

Notes : 
- The whole process can take up to ???min for ??? data.
- This program has been only test for Linux users.

## Authors

**Konrad WAGSTYL** (UCL GOSICH, London)\
**Sophie ADLER** (UCL GOSICH, London)\
**Mathilde RIPART** (UCL GOSICH, London)\


## References 
For any use of this code, the following paper must be cited :
???
