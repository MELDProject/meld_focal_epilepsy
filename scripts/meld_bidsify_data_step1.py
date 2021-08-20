import os 
import subprocess as sub
import glob 
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Script to bidsify MELD data. PART 1 : convert DICOMs into NIFTI')
    parser.add_argument('-d','--meld_folder', 
                        help='path to the meld_focal_epilepsy folder', 
                        required=True)
    args = parser.parse_args()

    meld_folder= args.meld_folder

    #information about meld_template 
    strengths=['15T', '3T', '7T']
    modalities = ['t1','postop_t1', 't2', 'flair', 'md', 'fa']
    
    #get participants folder 
    participants_folder = os.path.join(meld_folder,'participants')
    
    #load list participants
    participants = glob.glob(os.path.join(participants_folder,'MELD_*'))

    participants = [os.path.basename(x) for x in participants]

    #print information
    print('MELD_bidsify STEP 1 : convert dicoms into nifti')
    #loop over participants
    for participant in participants:
        print(f'start process for {participant}')

        # load in path of the specific participant
        path = os.path.join(participants_folder, participant)

        #loop over each folder in meld_template and convert dicoms into nifti when exist
        for T in strengths:
            for mod in modalities:
                dcm_folder=os.path.join(path,T,mod)
                if not os.path.isdir(dcm_folder):
                    print(f'folder {dcm_folder} does not exist. Check your participant folder is similar to the meld_template')
                elif  len(os.listdir(dcm_folder))==1 and os.listdir(dcm_folder)[0]=='.gitkeep':
                    pass
                else:
                    files_nii=glob.glob(os.path.join(dcm_folder,'*.nii*'))
                    name_base = '.'.join([T,mod])
                    name_nii = name_base+'.nii'
                    if files_nii:
                        print(f'Nifti file already exist in folder {dcm_folder}')
                    else:
                        command1= format(f"dcm2niix -f {name_base} -o {dcm_folder} {dcm_folder}")
                        f = os.path.join(dcm_folder,name_nii) 
                        try:
                            sub.check_call(command1, shell=True)
                        except:
                            print('Error in converting dicom into nifti. Check that your files are DICOMs format')
    #print information
    print('End of STEP 1. \n You can use the nifti file to create the lesion. \n Place the nifti lesion file into the lesion_mask folder')
