import os 
import subprocess as sub
import glob 
import json
import argparse
import pandas as pd
import shutil
import itertools
from joblib import Parallel, delayed
from datetime import datetime
import logging


#functions
def harmonise_bids_name(name):
    split = name.split('_')  
    #change FCD by P
    split = ['P' if x=='FCD' else x for x in split]
    #remove scanner information
    list_exclude = ["3T", "7T", "15T"]
    for l in list_exclude:
        try:
            split.remove(l)
        except:
            pass
    # exclude specific characters
    harmo_name= ''.join(split)
    
    return harmo_name

def create_json_file(name, info):
    dictionary = {
        "Modality": "MR",
        "MagneticFieldStrength": info['strength'],
        "ImagingFrequency": "n/a",
        "Manufacturer": "n/a",
        "PulseSequenceName": "n/a",
        "InternalPulseSequenceName": "n/a",
        "ManufacturersModelName": "n/a",
        "InstitutionName": "n/a",
        "DeviceSerialNumber": "n/a",
        "StationName": "n/a",
        "BodyPartExamined": "BRAIN",
        "PatientPosition": "n/a",
        "SoftwareVersions": "n/a",
        "MRAcquisitionType": "n/a",
        "SeriesDescription": "n/a",
        "ProtocolName": "n/a",
        "ScanningSequence": "n/a",
        "SequenceVariant": "n/a",
        "ScanOptions": "n/a",
        "ImageType": "n/a",
        "SeriesNumber": "n/a",
        "AcquisitionTime": "n/a",
        "AcquisitionNumber": "n/a",
        "SliceThickness": "n/a",
        "SpacingBetweenSlices": "n/a",
        "SAR": "n/a",
        "EchoTime": "n/a",
        "RepetitionTime": "n/a",
        "FlipAngle": "n/a",
        "PhaseEncodingPolarityGE": "n/a",
        "CoilString": "n/a",
        "PercentPhaseFOV": "n/a",
        "PercentSampling": "n/a",
        "AcquisitionMatrixPE": "n/a",
        "ReconMatrixPE": "n/a",
        "EffectiveEchoSpacing": "n/a",
        "TotalReadoutTime": "n/a",
        "PixelBandwidth": "n/a",
        "PhaseEncodingDirection": "n/a",
        "SliceTiming": "n/a",
        "ImageOrientationPatientDICOM": "n/a",
    }
    with open(name, 'w') as outfile:
        json.dump(dictionary, outfile)

        
def deface_and_sort_nii(T_mod, path, tmp_folder_participant):
    T=T_mod[0]
    mod=T_mod[1]
    dcm_folder=os.path.join(path,T,mod)
    if not os.path.isdir(dcm_folder):
        print(f'WARNING: folder {dcm_folder} does not exist. Check your participant folder is similar to the meld_template')
    elif not os.listdir(dcm_folder):
        pass
    else:
        files_nii=glob.glob(os.path.join(dcm_folder,'*.nii*'))
        name_base = '.'.join([T,mod])
        #if nifti file : copy nifti in tmp_dcm2bids and create fake json file
        if len(files_nii)==0:
            print(f'WARNING: No files found for modality {mod} at {T}. Skip')
        else:
            for f in files_nii:
                # skip process for the flair coregister file
                if 'coreg' in f:
                    print('INFO: skip process for FLAIR coreg')
                    continue
                # get the additional negPE file for dwi
                if 'negPE' in f:
                    name_nii = name_base+'_negPE'+'.nii.gz'
                    name_json = name_base+'_negPE'+'.json'
                else:
                    name_nii = name_base+'.nii.gz'
                    name_json = name_base+'.json'
		# gzip file if not zipped
                if not '.nii.gz' in f:
                    command = format(f'gzip {f}')
                    sub.check_call(command, shell=True)
                    f = f+'.gz'
                # deface file except if nodeface flag or if lesion mask
                if (args.nodeface==True) or (mod == 'lesion_mask'):
                    command = format(f'cp {f} {tmp_folder_participant}/{name_nii}')
                    sub.check_call(command, shell=True)
                    print(f'INFO : no deface. just copy nii {name_nii} in {tmp_folder_participant}')
                else:
                    command = format(f'pydeface --outfile {tmp_folder_participant}/{name_nii} {f} ')
                    try:   
                        sub.check_call(command, shell=True)
                        print(f'deface nifti {name_nii} and copy in {tmp_folder_participant}')
                    except:
                        print('ERROR : Error in defacing and copying nifti into temporary folder, please make sure FSL is installed')
                #if json file available copy it. If not create a fake one
                nii_base = f.split('.nii')[0]
                fjson = nii_base+'.json'
                print(fjson)
                if os.path.isfile(fjson):
                    command = format(f'cp {fjson} {tmp_folder_participant}/{name_json}')
                    print(command)
                    try:   
                        sub.check_call(command, shell=True)
                        print(f'INFO: just copy json {name_json} in {tmp_folder_participant}')
                    except:
                        print('ERROR: Error in copying json into temporary folder')
                else:
                    print('INFO: Creation of a json file into temporary folder')
                    info={}
                    info['strength']=T
                    json_file = os.path.join(tmp_folder_participant,name_json)
                    create_json_file(json_file,info)
            #if dwi modality, copy bval and bvec
            files_bvec=glob.glob(os.path.join(dcm_folder,'*.bvec'))   # for dwi files
            files_bval=glob.glob(os.path.join(dcm_folder,'*.bval'))   # for dwi files
            if mod=='dwi':
                if (len(files_bval)<1) or (len(files_bvec)<1):
                    print(f'WARNING: missing files bvec and bvals for modality dwi. Please check files \
                    are in the right folder {T}/{mod}')
                else:
                    name_bval = name_base+'.bval'
                    name_bvec = name_base+'.bvec'
                    fbval = files_bval[0]
                    fbvec = files_bvec[0]
                    command1 = format(f'cp {fbval} {tmp_folder_participant}/{name_bval}')
                    command2 = format(f'cp {fbvec} {tmp_folder_participant}/{name_bvec}')
                    try:   
                        sub.check_call(command1, shell=True)
                        print(f'INFO: just copy bval file {name_bval} in {tmp_folder_participant}')
                        sub.check_call(command2, shell=True)
                        print(f'INFO:just copy bvec file {name_bvec} in {tmp_folder_participant}')
                    except:
                        print('ERROR: Error in copying bval or bvec into temporary folder')
                    
                    
    return 

    
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Script to bidsify MELD data. PART 1 : convert DICOMs into NIFTI')
    parser.add_argument('-d','--meld_folder', 
                        help='Path to the meld_focal_epilepsy folder', 
                        required=True)
    parser.add_argument('-ids', '--list_participants',
                        help='Text file with participants ids to send',
                        required=True)
    parser.add_argument('-njobs',
                        help='precise number of cpu to use to run defacing in parallel. Default is all minus 1',
                        default = -2)
    parser.add_argument('--nodeface',
                        help='if flag, do not deface the NIFTI images',
                        action="store_true")
    parser.add_argument('--nodel',
                        help='if flag, do not delete the meldbids folder after compression',
                        action="store_true",)
    parser.add_argument('-v','--verbose', 
                        help='print issues',action='store_true',
                         default=False, 
                        )
    args = parser.parse_args()

    meld_folder= args.meld_folder
    list_participants = args.list_participants
    QUIET =args.verbose
    logging.basicConfig(level=logging.WARNING if QUIET else logging.INFO,
                    format="%(message)s")
    
    #information about meld_template 
    strenghts=['15T', '3T', '7T']
    modalities = ['t1','postop_t1', 't2', 'flair', 'dwi','lesion_mask']
    T_mod = list(itertools.product(*[strenghts,modalities]))
    
    #create a meldBIDS folder with today date
    now =  datetime.now()
    date = now.strftime("%d%m%Y")
    folder_name = f'meldbids_{date}'
    bids_folder = os.path.join(meld_folder,'meld_bids',folder_name)
    if not os.path.exists(bids_folder):
            os.makedirs(bids_folder)

    #folder to store nifti and json file for dcm2bids
    tmp_folder = os.path.join(bids_folder, 'tmp_dcm2bids')
    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)

    #load participants from list 
    f = open(list_participants, 'r')
    participants = f.readlines()
    participants = [x.strip() for x in participants] 
    print(participants)

    #print information
    print('MELD_bidsify STEP 2 : Deface nifti, convert into BIDS format and create compressed batch files.')
    
    #get participants folder 
    participants_folder = os.path.join(meld_folder,'participants')
    
    #loop over participants
    for participant in participants:

        #rename participant
        participant_bids = harmonise_bids_name(participant)

        #load in path of the specific participant
        path = os.path.join(participants_folder, participant)

        #create the temporary folder of the participants
        tmp_folder_participant= os.path.join(tmp_folder, 'sub-' + participant_bids)
        if not os.path.exists(tmp_folder_participant):
            os.makedirs(tmp_folder_participant)
        
        # Parallelise for each strenght_modality (n_jobs=1 means: use all available cores)
        print(f'INFO: Parallelise defacing with {str(args.njobs)} jobs')
        element_information = Parallel(n_jobs=int(args.njobs))(delayed(deface_and_sort_nii)(node, path, tmp_folder_participant) for node in T_mod)
        #convert in bids structure using dcm2bids
        config_file = os.path.join(meld_folder,'meld_dcm2bids_config.json')
        command=format(f'dcm2bids -d {participants_folder} -p {participant_bids} -c {config_file} -o {bids_folder}')
        try:
            sub.check_call(command, shell=True)
            print('INFO: convert into bids structure')
        except:
            print('ERROR: Error in converting in bids structure')
        
        #delete tmp folder 
        shutil.rmtree(tmp_folder)
        
        #compression in batch
        print(f'INFO: Compress {bids_folder}')
        command=format(f'cd {meld_folder}/meld_bids ; zip -r {folder_name} {folder_name} ; split -b 800000000  {folder_name}.zip share_data_part_')
        sub.check_call(command, shell=True)
        
        # do not delete meldbids folder if flag
        if args.nodel==False:
            shutil.rmtree(bids_folder)
            
        print('End of STEP 2' )
