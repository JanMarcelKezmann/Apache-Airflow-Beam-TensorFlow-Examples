import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import cv2
import pathlib
import numpy as np
import tensorflow as tf
from PIL import Image
import constants

data_dir = "data/"
train_img_dir = os.path.join(data_dir, "images_prepped_train/")
test_img_dir = os.path.join(data_dir, "images_prepped_test/")

train_mask_dir = os.path.join(data_dir, "annotations_prepped_train/")
test_mask_dir = os.path.join(data_dir, "annotations_prepped_test/")

tfrecords_dir = os.path.join(data_dir, "tfrecords")
train_record_file = os.path.join(tfrecords_dir, "train/train.tfrecords")
test_record_file = os.path.join(tfrecords_dir, "test/test.tfrecords")


pathlib.Path(tfrecords_dir).mkdir(parents=True, exist_ok=True)
pathlib.Path(os.path.join(tfrecords_dir, "train")).mkdir(parents=True, exist_ok=True)
pathlib.Path(os.path.join(tfrecords_dir, "test")).mkdir(parents=True, exist_ok=True)

def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy() # BytesList won't unpack a string from an EagerTensor.
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _int64_feature(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def image_example(img_string, mask_string):
    """Returns tf.Example containing image and mask as byteslist
    

    Args:
        img_string: bytes string of image
        mask_string: bytes string of mask

    Returns:
        tf.train.Example which will be serialized and written to tfrecord
    """
    feature = {
        constants.IMAGE_KEY: _bytes_feature(img_string),
        constants.MASK_KEY: _bytes_feature(mask_string)
    }

    return tf.train.Example(features=tf.train.Features(feature=feature))


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
        res = cv2.resize(img, dsize=(height, width))
        cv2.imwrite(filepath, res)
        print("{} resized from shape {} to shape (360, 480, 3)".format(filepath, (h, w, d)))

def write_files_to_tfrecord(record_file, img_dir, mask_dir, height, width):
    """Write train files to TFRecord
    
    Args:
        record_file: String of filepath the tfrecordwriter should write to
        img_dir: String of directory of images
        mask_dir: String of directory of masks
        height: Int
        width: Int

    Returns:
        None
    """
    with tf.io.TFRecordWriter(record_file) as writer:
        for num, filename in enumerate(sorted(os.listdir(img_dir))):
                if num % 100 == 0:
                    print("Image number {}".format(num))

                resize_and_save_image(os.path.join(img_dir, filename), height, width)
                resize_and_save_image(os.path.join(mask_dir, filename), height, width)

                image_string = open(os.path.join(img_dir, filename), "rb").read()
                mask_string = open(os.path.join(mask_dir, filename), "rb").read()
                tf_example = image_example(image_string, mask_string)
                writer.write(tf_example.SerializeToString())

write_files_to_tfrecord(train_record_file, train_img_dir, train_mask_dir, 360, 480)
write_files_to_tfrecord(test_record_file, test_img_dir, test_mask_dir, 360, 480)