import os 
import subprocess as sub
import glob 
import json
import argparse
import pandas as pd
import shutil
from datetime import datetime


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

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Script to bidsify MELD data. PART 1 : convert DICOMs into NIFTI')
    parser.add_argument('-d','--meld_folder', 
                        help='Path to the meld_focal_epilepsy folder', 
                        required=True)
    parser.add_argument('-ids', '--list_participants',
                        help='Text file with participants ids to send',
                        required=True)
    parser.add_argument('--nodeface',
                        help='if flag, do not deface the NIFTI images',
                        action="store_true")
    parser.add_argument('--nodel',
                        help='if flag, do not delete the meldbids folder after compression',
                        action="store_true")
    args = parser.parse_args()

    meld_folder= args.meld_folder
    list_participants = args.list_participants

    #information about meld_template 
    strenghts=['15T', '3T', '7T']
    modalities = ['t1','postop_t1', 't2', 'flair', 'dwi']
    
    #create a meldBIDS folder with today date
    now =  datetime.now()
    date = now.strftime("%d%m%Y")
    bids_folder = os.path.join(meld_folder,'meld_bids',f'meldbids_{date}')
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
    
    #print information
    print('MELD_bidsify STEP 2 : Deface nifti, convert into BIDS format and create compressed batch files.')
    
    #get participants folder 
    participants_folder = path = os.path.join(meld_folder,'participants')
    
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
        
        #loop over each folder in meld_template
        for T in strenghts:
            for mod in modalities:
                dcm_folder=os.path.join(path,T,mod)
                if not os.path.isdir(dcm_folder):
                    print(f'folder {dcm_folder} does not exist. Check your participant folder is similar to the meld_template')
                if not os.listdir(dcm_folder):
                    pass
                else:
                    files_nii=glob.glob(os.path.join(dcm_folder,'*.nii*'))
                    files_json=glob.glob(os.path.join(dcm_folder,'*.json'))
                    name_base = '.'.join([T,mod])
                    name_nii = name_base+'.nii'
                    name_json = name_base+'.json'
                    #if nifti file : copy nifti in tmp_dcm2bids and create fake json file
                    if len(files_nii)>1:
                        print('WARNING: There should be only one nifti file. Check again and remove additional file.')
                    elif len(files_nii)==1:
                        f = files_nii[0] 
                        if args.nodeface==True:
                            command = format(f'cp {f} {tmp_folder_participant}/{name_nii}')
                        else:
                            command = format(f'pydeface --outfile {tmp_folder_participant}/{name_nii} {f} ')
                        try:   
                            sub.check_call(command, shell=True)
                            print(f'deface nifti {name_nii} and copy in {tmp_folder_participant}')
                        except:
                            print('Error in defacing and copying nifti into temporary folder, please make sure FSL is installed')
                        #if json file available copy it. If not create a fake one
                        if len(files_json)>1:
                            print('WARNING: There should be only one json file. Check again and remove additional file.')
                        elif len(files_json)==1:
                            f = files_json[0] 
                            command = format(f'cp {f} {tmp_folder_participant}/{name_json}')
                            try:   
                                sub.check_call(command, shell=True)
                                print(f'just copy json {name_json} in {tmp_folder_participant}')
                            except:
                                print('Error in copying json into temporary folder')
                        else:
                            print('Creation of a json file into temporary folder')
                            info={}
                            info['strength']=T
                            json_file = os.path.join(tmp_folder_participant,name_json)
                            create_json_file(json_file,info)
                    else:
                        pass


        #convert in bids structure using dcm2bids
        config_file = os.path.join(meld_folder,'scripts','meld_dcm2bids_config.json')
        command=format(f'dcm2bids -d {participants_folder} -p {participant_bids} -c {config_file} -o {bids_folder}')
        try:
            sub.check_call(command, shell=True)
            print('convert into bids structure')
        except:
            print('Error in converting in bids structure')
        
        #delete tmp folder 
        shutil.rmtree(tmp_folder)
        
        #compression in batch
        print(f'Compress {bids_folder}')
        command=format(f'zip -r {bids_folder} {bids_folder}; split -b 800M {bids_folder}.zip {bids_folder}/share_data_part')
        sub.check_call(command, shell=True)
        
        #delete meldbids folder if flag
        if args.nodel==True:
            shutil.rmtree(bids_folder)
            
        print('End of STEP 2' )
