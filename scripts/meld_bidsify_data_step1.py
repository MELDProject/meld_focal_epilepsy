import os 
import subprocess as sub
import glob 
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Script to bidsify MELD data. PART 1 : convert DICOMs into NIFTI')
    parser.add_argument('-d','--part_dir', 
                        help='path to participants directory', 
                        required=True)
    args = parser.parse_args()

    folder_participants= args.part_dir

    #information about meld_template 
    strenghts=['15T', '3T', '7T']
    modalities = ['t1','postop_t1', 't2', 'flair', 'md', 'fa']

    #load list participants
    participants = glob.glob(os.path.join(folder_participants,'MELD*'))
    participants = [os.path.basename(x) for x in participants]

    #print information
    print('MELD_bidsify STEP 1 : convert dicoms into nifti')

    #loop over participants
    for participant in participants:
        print(f'start process for {participant}')

        # load in path of the specific participant
        path = os.path.join(folder_participants, participant)

        #loop over each folder in meld_template and convert dicoms into nifti when exist
        for T in strenghts:
            for mod in modalities:
                dcm_folder=os.path.join(path,T,mod)
                if not os.path.isdir(dcm_folder):
                    print(f'folder {dcm_folder} does not exist. Check your participant folder is similar to the meld_template')
                if not os.listdir(dcm_folder):
                    pass
                else:
                    files_nii=glob.glob(os.path.join(dcm_folder,'*.nii*'))
                    files_dcm=glob.glob(os.path.join(dcm_folder,'*.dcm'))
                    name_base = '.'.join([T,mod])
                    name_nii = name_base+'.nii'
                    if files_nii:
                        print(f'Nifti file already exist in folder {dcm_folder}')
                    elif len(files_dcm)>1:  
                        command1= format(f"dcm2niix -f {name_base} -o {dcm_folder} {dcm_folder}")
                        f = os.path.join(dcm_folder,name_nii) 
                        try:
                            sub.check_call(command1, shell=True)
                        except:
                            print('Error in converting dicom into nifti')
                    else:
                        pass
    #print information
    print('End of STEP 1. \n You can use the nifti file to create the lesion. \n Place the nifti lesion file into the right folder')
