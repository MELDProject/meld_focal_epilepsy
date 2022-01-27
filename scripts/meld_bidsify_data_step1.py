import os 
import subprocess as sub
import glob 
import argparse
import logging


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Script to bidsify MELD data. PART 1 : convert DICOMs into NIFTI')
    parser.add_argument('-d','--meld_folder', 
                        help='path to the meld_focal_epilepsy folder', 
                        required=True)
    parser.add_argument('-v','--verbose', 
                        help='print issues',action='store_true',
                         default=False, 
                        )
    args = parser.parse_args()
    QUIET =args.verbose
    logging.basicConfig(level=logging.WARNING if QUIET else logging.INFO,
                    format="%(message)s")
    meld_folder= args.meld_folder

    #information about meld_template 
    strengths=['15T', '3T', '7T']
    modalities = ['t1','postop_t1', 't2', 'flair', 'dwi']
    
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
                        print(f'WARNING: Nifti file already exist in folder {dcm_folder}')
                    else:
                        command1= format(f"dcm2niix -f {name_base} -o {dcm_folder} {dcm_folder} -v n")
                        f = os.path.join(dcm_folder,name_nii) 
                        try:
                            if args.verbose:
                                sub.check_call(command1, shell=True)
                            else:
                                sub.check_call(command1, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        except:
                            #print('Error in converting dicom into nifti. Check that your files are DICOMs format')
                            pass
    #print information
    print('End of STEP 1. \n You can use the nifti file to create the lesion. \n Place the nifti lesion file into the lesion_mask folder')
