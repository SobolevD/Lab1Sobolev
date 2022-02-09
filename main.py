import json

import numpy as np
from matplotlib import pyplot as plt
from skimage import transform
from skimage.exposure import histogram
from skimage.io import imread
from skimage.io import imshow


def read_parameters(file_path):
    # Open file with parameters
    with open(file_path) as json_file:
        json_data = json.load(json_file)

    # Log
    for entry in json_data.keys():
        print(f'Got parameter "{entry}" with value = "{json_data[entry]}"')
    return json_data


def read_image(file_path):
    # Open file with image
    img = imread(file_path)
    # Log
    print('Image shape: ', img.shape)
    return img


def affine_transform_image(img, scale_xy, shift_xy, angle):
    tform = transform.AffineTransform(
        scale=scale_xy,
        translation=shift_xy,
        rotation=angle
    )
    # Log
    print(tform.params)
    tf_img = transform.warp(img, tform)
    return tf_img


def create_union_plot(img1, img2):
    fig = plt.figure(figsize=(10, 5))
    fig.add_subplot(2, 2, 1)
    imshow(img1)
    fig.add_subplot(2, 2, 2)
    imshow(img2)
    fig.add_subplot(2, 2, 3)
    create_histogram_plot(img1)
    fig.add_subplot(2, 2, 4)
    create_histogram_plot(img2)
    return fig


def create_histogram_plot(img_array):
    hist_red, bins_red = histogram(img_array[:, :, 2])
    hist_green, bins_green = histogram(img_array[:, :, 1])
    hist_blue, bins_blue = histogram(img_array[:, :, 0])

    plt.ylabel('Number of counts')
    plt.xlabel('Brightness')
    plt.title('Histogram of the brightness distribution for each channel')
    plt.plot(bins_green, hist_green, color='green', linestyle='-', linewidth=1)
    plt.plot(bins_red, hist_red, color='red', linestyle='-', linewidth=1)
    plt.plot(bins_blue, hist_blue, color='blue', linestyle='-', linewidth=1)
    plt.legend(['green', 'red', 'blue'])


def main():
    parameters = read_parameters('resources/application_properties.json')

    v_img = read_image(parameters['source_image_path'])

    v_scale_xy = parameters['scale_XY']
    v_shift_xy = parameters['shift_XY']
    v_angle = parameters['angle']

    v_result = affine_transform_image(v_img, v_scale_xy, v_shift_xy, v_angle)

    v_plot_result = create_union_plot(v_img, v_result)

    v_plot_result.savefig(parameters['destination_image_path'])

