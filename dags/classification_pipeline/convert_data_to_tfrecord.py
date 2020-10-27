import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import cv2
import pathlib
import numpy as np
import tensorflow as tf
from PIL import Image
import constants

data_dir = "data/"
train_dir = os.path.join(data_dir, "Image_Classification/seg_train")
# test_dir = os.path.join(data_dir, "Image_Classification/seg_test")

tfrecords_dir = os.path.join(data_dir, "tfrecords")
train_record_file = os.path.join(tfrecords_dir, "train/train.tfrecords")
# test_record_file = os.path.join(tfrecords_dir, "test/test.tfrecords")


pathlib.Path(tfrecords_dir).mkdir(parents=True, exist_ok=True)
pathlib.Path(os.path.join(tfrecords_dir, "train")).mkdir(parents=True, exist_ok=True)
# pathlib.Path(os.path.join(tfrecords_dir, "test")).mkdir(parents=True, exist_ok=True)

def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy() # BytesList won't unpack a string from an EagerTensor.
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _int64_feature(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def image_example(img_string, label):#, height, width, depth):
    # image_shape = tf.image.decode_jpg(img_string).shape
    # label_shape = tf.image.decode_jpg(lbl_string).shape

    feature = {
        # "height": _int64_feature(height),
        # "width": _int64_feature(width),
        # "depth": _int64_feature(depth),
        "label": _int64_feature(label),
        "image_raw": _bytes_feature(img_string),
    }

    return tf.train.Example(features=tf.train.Features(feature=feature))

def get_label_from_directory(directory):
    """
    Function to set the label for each image. In our case, we'll use the file 
    path of a label indicator. Based on your initial data 
    
    Args:
        directory: string
    
    Returns:
        int - label
    
    Raises:
        NotImplementedError if unknown image class is detected
    
    """

    lowered_directory = directory.lower()
    if "buildings" in lowered_directory:
        label = 0
    elif "forest" in lowered_directory:
        label = 1
    elif "glacier" in lowered_directory:
        label = 2
    elif "mountain" in lowered_directory:
        label = 3
    elif "sea" in lowered_directory:
        label = 4
    elif "street" in lowered_directory:
        label = 5
    else:
        raise NotImplementedError("Found unknown image")
    return label

def resize_and_save_image(filepath, height, width):
    """Function to resize and save images which do not have the prespecified image shape of (height, width, 3).

    Args:
        filepath: String of imagepath
        height: Int
        width: Int

    Returns:
        None

    """
    img = cv2.imread(filepath)
    h, w, d = img.shape
    if h != height or w != width:
        res = cv2.resize(img, dsize=(150, 150))
        cv2.imwrite(filepath, res)
        print("{} resized from shape {} to shape (150, 150, 3)".format(filepath, (h, w, d)))
    if d != 3:
        print(filepath)

# Write train files to TFRecord
with tf.io.TFRecordWriter(train_record_file) as writer:
    for dir_num, directory in enumerate(sorted(os.listdir(train_dir))):
        for img_num, filename in enumerate(sorted(os.listdir(os.path.join(train_dir, directory)))):
            if img_num % 299 == 0:
                print("Directory number {} and Image number {}".format(dir_num, img_num))

            resize_and_save_image(os.path.join(train_dir, directory, filename), 150, 150)

            # ToDo: put an assert operator in here to check if every image and mask has the same shape
            # image_string = image.tobytes()

            image_string = open(os.path.join(train_dir, directory, filename), "rb").read()
            label = get_label_from_directory(directory)
            tf_example = image_example(image_string, label)#, height, width, depth)
            writer.write(tf_example.SerializeToString())

# Write test files to TFRecord
# with tf.io.TFRecordWriter(test_record_file) as writer:
#     for dir_num, directory in enumerate(sorted(os.listdir(test_dir))):
#         for img_num, filename in enumerate(sorted(os.listdir(os.path.join(test_dir, directory)))):
#             if img_num % 200 == 0:
#                 print("Directory number {} and Image number {}".format(dir_num, img_num))

#             image = np.array(Image.open(os.path.join(test_dir, directory, filename)))
#             # height, width, depth = image.shape

#             # ToDo: put an assert operator in here to check if every image and mask has the same shape

#             image_string = image.tobytes()

#             label = get_label_from_directory(directory)

#             tf_example = image_example(image_string, label)#, height, width, depth)

#             writer.write(tf_example.SerializeToString())