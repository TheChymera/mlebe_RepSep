from nilearn.plotting import plot_anat
from samri.plotting.maps import scaled_plot
import matplotlib.pyplot as plt

fig = plt.figure()
template = '/usr/share/mouse-brain-atlases/ambmc_40micron.nii'
scaled_plot(template,
        cut=(0,0,0,),
        threshold=200000,
        cmap='gray',
        scale=0.2,
        dim=0.1,
        fig=fig
        )
