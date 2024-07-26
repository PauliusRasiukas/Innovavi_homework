import json
import os

import numpy as np
import pandas as pd

from PIL import Image
from matplotlib import pyplot as plt
from scipy.spatial import ConvexHull


def plot_mask_over_image(row_data, parameter_name, filter_value):

    with open(f"data/clean_parameter_set/{str.lower(row_data.camera_type)}_data_{parameter_name}", "r") as f:
        parameter_data = json.load(f)

    parameter_top = [d for d in parameter_data if d['parameters'][parameter_name] > row_data[parameter_name]][0]
    parameter_bot = [d for d in parameter_data if d['parameters'][parameter_name] < row_data[parameter_name]][-1]

    index_difference = pd.DataFrame(parameter_top['indexes']) - pd.DataFrame(parameter_bot['indexes'])
    columns_sum = index_difference.sum()[index_difference.abs().sum() > filter_value].index.to_list()
    index_coords = [row_data[[s + '_x' for s in columns_sum]].reset_index(drop=True),
                    row_data[[s + '_y' for s in columns_sum]].reset_index(drop=True)]
    index_coords = pd.concat(index_coords, axis=1)

    img = Image.open(f'data/train_set/batch01/Rendering/Render_{row_data.id}_{row_data.camera_type}.png')
    img2 = np.asarray(img).copy()

    image_pixel_coords = index_coords.to_numpy() / 2
    hull = ConvexHull(image_pixel_coords)
    plt.imshow(img2, interpolation='nearest')
    plt.fill(image_pixel_coords[hull.vertices, 0], image_pixel_coords[hull.vertices, 1], 'g', alpha=0.5)

    if not os.path.exists('results/'):
        os.makedirs('results/')
    plt.savefig(f'results/Render_{row_data.id}_{row_data.camera_type}_{parameter_name}.png')
    plt.close()
