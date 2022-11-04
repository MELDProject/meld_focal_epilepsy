# MELD project –  meld_focal_epilepsy

 `meld_focal_epilepsy`  – convert MELD dataset into a BIDS structure and send to the MELD team. 

## Overview
This program performs three steps :
 1. DICOMS TO NIFTI : Goes over the meld_template folder and convert DICOMs into NIFTI. Results save as nifti format (.nii). 
 2. NIFTI TO BIDS : Data are copied over a temporary folder and defaced. Data are converted into BIDS format using dcm2bids.
 3. COMPRESSION : BIDS folder is compressed and send over to the MELD team.

More detailled guidelines can be found in our [Protocol 2 - MRI data protocol](https://www.protocols.io/view/protocol-2-mri-data-protocol-3byl4k8jjvo5/v1) on **Protocols.io**.
  
## Getting Started

### Prerequisites
This program requires the following softwares and libraries : 
- FSL 6.0 ([installation guidelines](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation))
- Anaconda ([installation guidelines](https://www.anaconda.com/products/individual-d))


### Installation
- [ ] Open a terminal and paste the following sentence : 
     ```bash
     git clone https://github.com/MELDProject/meld_focal_epilepsy
     ```
     Press enter. Your package will be installed. 
- [ ] Create the conda environment: 
```bash
cd <path_to_meld_focal_epilepsy_github_folder>/meld_focal_epilepsy/scripts 
conda env create -f mfe_env.yml 
```
Your meld_focal_epilepsy package is ready to be used and you can activate it with :
```bash
conda activate mfe_env
```

Note : you will have to activate your environment every time you open a new terminal and you want to use the meld_focal_epilepsy package

## Usage
### 1) Prepare the MELD data
Prepare your data following the MELD Focal Epilepsy architecture detailled at [Protocol 2 - MRI data protocol](https://www.protocols.io/view/protocol-2-mri-data-protocol-3byl4k8jjvo5/v1) \

  a. Download the meld_focal_epilepsy_data folder from : https://figshare.com/s/763e50f4eb51a4f76f58 \
  b. Copy the meld_template folder and rename with the MELD participant ID \
  c. Fill the folders with DICOMS/NIFTI from the respective sequences available (e.g T1w sequence acquired at 3T should go into the MELD_participantID/3T/T1/ folder) 

### 2) Convert DICOMs into NIFTI 
To launch the script, run 
```bash
cd <path_to_meld_focal_epilepsy_github_folder>/meld_focal_epilepsy/scripts
python meld_bidsify_data_step1.py -d <path_to_meld_focal_epilepsy_data_folder>
```
where : 
   - `<path_to_meld_focal_epilepsy_github_folder>` : the path to where your meld_focal_epilepsy folder has been saved
   - `<path_to_meld_focal_epilepsy_data_folder>` : the path to where your data are stored

### 3) Create the lesion mask 
Create the lesion mask from the NIFTI T1 volume if not already done. Save the lesion mask as NIFTI into the right folder.

See [Protocol 2 - MRI data protocol](https://www.protocols.io/view/protocol-2-mri-data-protocol-3byl4k8jjvo5/v1) for more detailled guidelines on how to create the lesion mask

### 5) Convert NIFTI into BIDS format for the participants you which to send over. 
You will need to create a list of participant in a text file 
 e.g.
     MELD_H1_3T_P_0001
     MELD_H1_3T_P_0002
     MELD_H1_15T_P_0001
     MELD_H1_15T_C_0002
To launch the script, run 
```bash
cd <path_to_meld_focal_epilepsy_github_folder>/meld_focal_epilepsy/scripts
python meld_bidsify_data_step2.py -d <path_to_meld_focal_epilepsy_data_folder> -ids <list_participants.txt> [optional argument]
```

where : 
   - `<path_to_meld_focal_epilepsy_github_folder>` : the path to where your meld_focal_epilepsy folder has been saved
   - `<path_to_meld_focal_epilepsy_data_folder>` : the path to where your data are stored
  - `<list_participants.txt>` : the path to the txt file containing the list of participant's ids you wish to share with the MELD team
  - optional arguments:
    - `-njobs <number>` : number of cpu to parallelise defacing (num, -1: all, -2: all minus 1)
    - `--nodeface` : use this flag if you do not need to deface your NIFTI images.
    - `--nodel` : use this flag if you do not want to the temporary folder to be deleted 
    - `-v` : use this flag to print more warning/error information


Notes : 
- This program has been only test for Linux users.


## Example :
Activate Anaconda environment
```bash
conda activate mfe_env 
```
Run meld_bidsify scripts
```bash
 cd /home/documents/meld_focal_epilepsy/scripts
 python meld_bidsify_data_step1.py -d /home/documents/meld_focal_epilepsy_data
 ```
Then create lesion masks \
Then run the second bidsify step
```bash
 cd /home/documents/meld_focal_epilepsy/scripts
 python meld_bidsify_data_step2.py -d /home/documents/meld_focal_epilepsy_data/ -ids /home/documents/meld_focal_epilepsy/participants/list_participants_batch_01072022.csv
```
 
## Authors

**Konrad WAGSTYL** (UCL GOSICH, London)\
**Sophie ADLER** (UCL GOSICH, London)\
**Mathilde RIPART** (UCL GOSICH, London)\


