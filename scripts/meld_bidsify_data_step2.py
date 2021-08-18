import os 
import subprocess as sub
import glob 
import json
import argparse


#functions
def harmonise_bids_name(name):
    split = name.split('_')
    print(split)
    
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
        "MagneticFieldStrength": info['strengh'],
        "ImagingFrequency": "NaN",
        "Manufacturer": "NaN",
        "PulseSequenceName": "NaN",
        "InternalPulseSequenceName": "NaN",
        "ManufacturersModelName": "NaN",
        "InstitutionName": "NaN",
        "DeviceSerialNumber": "NaN",
        "StationName": "NaN",
        "BodyPartExamined": "BRAIN",
        "PatientPosition": "NaN",
        "SoftwareVersions": "NaN",
        "MRAcquisitionType": "NaN",
        "SeriesDescription": "NaN",
        "ProtocolName": "NaN",
        "ScanningSequence": "NaN",
        "SequenceVariant": "NaN",
        "ScanOptions": "NaN",
        "ImageType": "NaN",
        "SeriesNumber": "NaN",
        "AcquisitionTime": "NaN",
        "AcquisitionNumber": "NaN",
        "SliceThickness": "NaN",
        "SpacingBetweenSlices": "NaN",
        "SAR": "NaN",
        "EchoTime": "NaN",
        "RepetitionTime": "NaN",
        "FlipAngle": "NaN",
        "PhaseEncodingPolarityGE": "NaN",
        "CoilString": "NaN",
        "PercentPhaseFOV": "NaN",
        "PercentSampling": "NaN",
        "AcquisitionMatrixPE": "NaN",
        "ReconMatrixPE": "NaN",
        "EffectiveEchoSpacing": "NaN",
        "TotalReadoutTime": "NaN",
        "PixelBandwidth": "NaN",
        "PhaseEncodingDirection": "NaN",
        "SliceTiming": "NaN",
        "ImageOrientationPatientDICOM": "NaN",
    }
    with open(name, 'w') as outfile:
        json.dump(dictionary, outfile)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Script to bidsify MELD data. PART 1 : convert DICOMs into NIFTI')
    parser.add_argument('-d','--part_dir', 
                        help='path to participants directory', 
                        required=True)
    parser.add_argument('-ids', '--list_part',
                        help='texte file with participants ids',
                        required=False,
                        default=os.getcwd())
    args = parser.parse_args()

    folder_participants= args.part_dir
    list_participants = args.list_part

    #information about meld_template 
    strenghts=['15T', '3T', '7T']
    modalities = ['t1','postop_t1', 't2', 'flair', 'md', 'fa']
    
    #create a temporary folder to store nifti and json file for dcm2bids
    tmp_folder = os.path.join(folder_participants, 'tmp_dcm2bids')
    if not os.path.exists(tmp_folder):
            os.makedirs(tmp_folder)

    #load list participants
    if list_participants :
        f = open(list_participants, 'r')
        participants = f.readlines()
        participants = [x.strip() for x in participants]
    else:
        participants = glob.glob(os.path.join(folder_participants,'MELD*'))
        participants = [os.path.basename(x) for x in participants]

    #loop over participants
    for participant in participants:

        #rename participant
        participant_bids = harmonise_bids_name(participant)

        # load in path of the specific participant
        path = os.path.join(folder_participants, participant)

        #create the temporary folder of the participants
        tmp_folder_participant= os.path.join(tmp_folder, 'sub-' + participant_bids)
        if not os.path.exists(tmp_folder_participant):
                os.makedirs(tmp_folder_participant)

        #loop over each folder in meld_template
        for T in strenghts:
            for mod in modalities:
                print(mod + ' ' + T)
                dcm_folder=os.path.join(path,T,mod)
                if not os.path.isdir(dcm_folder):
                    print(f'folder {dcm_folder} does not exist. Check your participant folder is similar to the meld_template')
                if not os.listdir(dcm_folder):
                    pass
                else:
                    files_nii=glob.glob(os.path.join(dcm_folder,'*.nii'))
                    files_json=glob.glob(os.path.join(dcm_folder,'*.json'))
                    name_base = '.'.join([T,mod])
                    name_nii = name_base+'.nii'
                    name_json = name_base+'.json'
                    #if nifti file : copy nifti in tmp_dcm2bids and create fake json file
                    if len(files_nii)>1:
                        print('There should be only one nifti file. Check again and remove additional file.')
                    elif len(files_nii)==1:
                        f = files_nii[0] 
                        command = format(f'cp {f} {tmp_folder_participant}/{name_nii}')
                        try:   
                            sub.check_call(command, shell=True)
                            print(f'just copy nifti {name_nii} in {tmp_folder_participant}')
                        except:
                            print('Error in copying nifti into temporary folder')
                        #if json file available copy it,if not create a fake one
                        if len(files_nii)>1:
                            print('There should be only one json file. Check again and remove additional file.')
                        elif len(files_json)==1:
                            f = files_json[0] 
                            command = format(f'cp {f} {tmp_folder_participant}/{name_json}')
                            try:   
                                sub.check_call(command, shell=True)
                                print(f'just copy nifti {name_json} in {tmp_folder_participant}')
                            except:
                                print('Error in copying json into temporary folder')
                        else:
                            print('Creation of a json file into temporary folder')
                            info={}
                            info['strengh']=T
                            json_file = os.path.join(tmp_folder_participant,name_json)
                            create_json_file(json_file,info)
                    else:
                        pass


        #convert in bids structure using dcm2bids
        config_file = os.path.join(folder_participants,'meld_dcm2bids_config.json')
        command=format(f'dcm2bids -d {folder_participants} -p {participant_bids} -c {config_file} -o {folder_participants} ')
        try:
            sub.check_call(command, shell=True)
            print('convert into bids structure')
        except:
            print('Error in converting in bids structure')
