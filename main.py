import pandas as pd

from parameter_set_processing import prepare_data
from plot_mask import plot_mask_over_image

root_parameter_path = 'data/parameter_set'
root_train_path = 'data/train_set/'

prepare_data(f'{root_parameter_path}/batch01', 'Brows Arch')
prepare_data(f'{root_parameter_path}/batch02', 'Brows Centre Depth')

train_data = pd.read_csv(f'{root_train_path}/batch01/batch01.csv', index_col=0)
train_data.apply(lambda row: plot_mask_over_image(row, 'Brows Arch', 0.001), axis=1)
train_data.apply(lambda row: plot_mask_over_image(row, 'Brows Centre Depth', 0.001), axis=1)

