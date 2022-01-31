import os 
import subprocess as sub
import glob 
import argparse
import logging


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Script to bidsify MELD data. PART 1 : convert DICOMs into NIFTI')
    parser.add_argument('-d','--meld_folder', 
                        help='path to the meld_focal_epilepsy_data folder containing data', 
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
        print(f'INFO: start process for {participant}')

        # load in path of the specific participant
        path = os.path.join(participants_folder, participant)

        #loop over each folder in meld_template and convert dicoms into nifti when exist
        for T in strengths:
            for mod in modalities:
                dcm_folder=os.path.join(path,T,mod)
                if not os.path.isdir(dcm_folder):
                    print(f'WARNING: folder {dcm_folder} does not exist. Check your participant folder is similar to the meld_template')
                else:
                    files_nii=glob.glob(os.path.join(dcm_folder,'*.nii*'))
                    files_dcm=glob.glob(os.path.join(dcm_folder,'*.dcm*'))
                    name_base = '.'.join([T,mod])
                    name_nii = name_base+'.nii'
                    if files_nii:
                        print(f'WARNING: Nifti file already exist in folder {dcm_folder}')
                    elif files_dcm:
                        command1= format(f"dcm2niix -f {name_base} -o {dcm_folder} {dcm_folder}")
                        f = os.path.join(dcm_folder,name_nii) 
                        if args.verbose:
                            sub.check_call(command1, shell=True)
                        else:
                            sub.check_call(command1, shell=True, stdout=sub.DEVNULL, stderr=sub.DEVNULL)
                        print(f'INFO: convert dcm in nifti {f}')
                    else:
                        pass
                    if mod=='flair':
                        print(f'INFO: Co-register FLAIR to T1 {T} for lesion masking')
                        files_nii=glob.glob(os.path.join(dcm_folder,'*.nii*'))
                        if 'coreg' in '-'.join(files_nii) :
                            print('INFO: FLAIR nifti file coregistered to T1 already exist. Skip')
                            pass
                        elif files_nii :
                            f_flair= files_nii[0]
                            f_flair_name_nii = name_base+'_coreg'+'.nii'
                            f_t1 = files_nii=glob.glob(os.path.join(path,T, 't1','*.nii*'))[0]
                            command1= format(f"flirt -in {f_flair} -ref {f_t1} -out {dcm_folder}/{f_flair_name_nii}")
                            if args.verbose:
                                sub.check_call(command1, shell=True)
                            else:
                                sub.check_call(command1, shell=True, stdout=sub.DEVNULL, stderr=sub.DEVNULL)
                            print(f'INFO: Registration done and saved at {dcm_folder}/{f_flair_name_nii}. You can use the FLAIR coreg to help create the lesion mask')
                        else:
                            pass
    #print information
    print('End of STEP 1. \n You can use the t1 nifti file (and flair coreg if available) to create the lesion. \n Place the nifti lesion file into the lesion_mask folder')
