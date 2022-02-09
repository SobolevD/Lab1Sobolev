import json

from PIL import Image
from skimage import transform
from skimage.io import imread, imsave


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


def save_image(img, file_path):
    # imageio.imwrite(file_path, img)#img.save(file_path, 'png')
    imsave(file_path, img)


parameters = read_parameters('resources/application_properties.json')

v_img = read_image(parameters['source_image_path'])
v_scale_xy = parameters['scale_XY']
v_shift_xy = parameters['shift_XY']
v_angle = parameters['angle']

v_result = affine_transform_image(v_img, v_scale_xy, v_shift_xy, v_angle)
im = Image.fromarray(v_result, 'RGB')

#fig, ax = plt.subplots()
#ax.imshow(v_result)
#show()

save_image(v_result, parameters['destination_image_path'])
