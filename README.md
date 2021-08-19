# MELD project –  meld_focal_epilepsy

 `meld_focal_epilepsy`  – convert MELD dataset into a BIDS structure and send to the MELD team. 

## Overview
This program performs three steps :
 1. DICOMS TO NIFTI : Goes over the meld_template folder and convert DICOMs into NIFTI. Results save as nifti format (.nii). 
 3. NIFTI TO BIDS : Data are copied over a temporary folder and defaced. Data are converted into BIDS format using dcm2bids.
 4. COMPRESSION : BIDS folder is compressed and send over to the MELD team.

  
## Getting Started

### Prerequisites
This program requires the following softwares and libraries : 
- Python (version 3.7)\
Libraries :
   - dcm2bids
- FSL 6.0


### Installation
- [ ] Open a terminal and paste the following sentence : `https://github.com/mathrip/meld_focal_epilepsy.git`
Press enter. Your package will be installed. 
- [ ] Install FSL :
- [ ] Open a new terminal \
Your meld_focal_epilepsy package is ready to be used. 

## Usage
1) Prepare the MELD data :\
    a. Copy the meld_template folder and rename with the MELD participant ID \
    b. Fill the folders with DICOMS/NIFTI from the respective sequences available (e.g T1w sequence acquired at 3T should go into the MELD_participantID/3T/T1/ folder)
2) Convert DICOMs into NIFTI. To launch the script, run \
`meld_bidsify_data_step1.py -d <participants_directory>`
3) Create the lesion mask from the NIFTI T1 volume if not already done. Save the lesion mask as NIFTI into the right folder.
5) Convert NIFTI into BIDS format for the participants you which to send over. To launch the script, run \
`meld_bidsify_data_step1.py -d <participants_directory> -ids <list_participants> [optional arguments]`

where : 
  - <meld_folder> : the path to the "meld_focal_epilepsy" directory.
  - <list_participants> : the path to the csv file containing the list of participant's ids you wish to share with the MELD team
  - optional arguments:
    - --nodeface : use this flag if you do not need to deface your NIFTI images.
    - --nodel (optional) : use this flag if you do not want to the temporary folder to be deleted 

Exemples :
- `python meld_bidsify_data_step1.py' -d '/home/documents/meld_focal_epilepsy/participants'`
- `python meld_bidsify_data_step2.py' -d '/home/documents/meld_focal_epilepsy/participants' -ids '/home/documents/meld_focal_epilepsy/participants/list_participants_batch.csv'`

Notes : 
- The whole process can take up to ???min for ??? data.
- This program has been only test for Linux users.

## Authors

**Konrad WAGSTYL** (UCL GOSICH, London)\
**sophie ADLER** (UCL GOSICH, London)\
**Mathilde RIPART** (UCL GOSICH, London)\


## References 
For any use of this code, the following paper must be cited :
???
