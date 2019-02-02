from itertools import product
from os import path
import os
from samri.report.snr import df_threshold_volume ,iter_threshold_volume
import nibabel as nib
import numpy as np
import pandas as pd
from bids.grabbids import BIDSLayout
from bids.grabbids import BIDSValidator
import nipype.interfaces.io as nio

def bids_autograb(bids_dir):
        bids_dir = path.abspath(path.expanduser(bids_dir))
        validate = BIDSValidator()
        layout = BIDSLayout(bids_dir)
        df = layout.as_data_frame()

        # Unclear in current BIDS specification, we refer to BOLD/CBV as modalities and func/anat as types
        df = df.rename(columns={'modality': 'type', 'type': 'modality'})
        return df

def avg_smoothness(inp_file):
        from nipype.interfaces import afni
        import numpy as np
        fwhm = afni.FWHMx()
        fwhm.inputs.in_file = inp_file
        fwhm.inputs.acf = True
        fwhm_run = fwhm.run()
        # It appears the new/correct FWHM is now located under the last position of the ACF estimates.
        # https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dFWHMx.html
        res = fwhm_run.outputs.acf_param[3]
        #mean_smoothness = np.asarray(res).mean()
        return res

def acqname(inp_entry):
        if('bold' in  inp_entry):
                return 'bold'
        else:
                return 'cbv'

scratch_dir = '~/data_scratch/irsabi'

df_generic = bids_autograb(scratch_dir + '/preprocessing/generic_collapsed/')
df_generic['Processing'] = 'Generic'
df_generic['Template'] = 'Generic'

df_generic_legacy = bids_autograb(scratch_dir + '/preprocessing/generic_ambmc_collapsed/')
df_generic_legacy['Processing'] = 'Generic'
df_generic_legacy['Template'] = 'Legacy'

df_legacy = bids_autograb(scratch_dir + '/preprocessing/legacy_collapsed/')
df_legacy['Processing'] = 'Legacy'
df_legacy['Template'] = 'Legacy'

df_legacy_generic = bids_autograb(scratch_dir + '/preprocessing/legacy_dsurqec_collapsed/')
df_legacy_generic['Processing'] = 'Legacy'
df_legacy_generic['Template'] = 'Generic'

df_bids = bids_autograb(scratch_dir + '/bids_collapsed/')
df_bids['Processing'] = 'Unprocessed'
df_bids['Template'] = 'Unprocessed'

df = pd.concat([df_generic, df_legacy, df_generic_legacy, df_legacy_generic, df_bids])
df['uID'] = df['subject']+'_'+df['session']+'_'+df['modality']

df = df.loc[np.logical_or(df.modality == 'cbv', df.modality == 'bold')]
df['acq'] = df['modality']

df['smoothness'] = df['path'].apply(avg_smoothness)
#df['acq'] = df['acquisition'].apply(acqname)

df['Smoothness Change Factor'] = ''
uids = df['uID'].unique()
for uid in uids:
	original = df.loc[(df['uID']==uid) & (df['Processing']=='Unprocessed'), 'smoothness'].item()
	df.loc[(df['uID']==uid), 'Smoothness Change Factor'] = df.loc[(df['uID']==uid), 'smoothness'] / original

files = os.listdir('./')
for _file in files:
        if  _file.endswith(('.out','.1D')):
                os.remove(path.abspath(path.expanduser(_file)))
