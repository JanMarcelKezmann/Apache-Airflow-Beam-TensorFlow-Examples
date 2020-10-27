import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from classification_pipeline import constants

from typing import List, Text, Dict, Union

import absl
import numpy as np
import tensorflow as tf
import tensorflow_transform as tft
from datetime import datetime

from tfx.components.trainer.executor import TrainerFnArgs


def _transformed_name(key: Text) -> Text:
    """Generate the name of the transformed feature from original name."""
    return key + "_xf"


def _gzip_reader_fn(filenames):
    """Small utility returning a record reader that can read gzip'ed files."""
    return tf.data.TFRecordDataset(filenames, compression_type='GZIP')


def _get_serve_image_fn(model):
  """Returns a function that feeds the input tensor into the model."""

  @tf.function
  def serve_image_fn(image_tensor):
    """Returns the output to be used in the serving signature.
    
    Args:
        image_tensor: A tensor represeting input image. The image should have 3
                      channels.
    
    Returns:
        The model's predicton on input image tensor
    """
    return model(image_tensor)

  return serve_image_fn


def preprocessing_fn(inputs: Dict[str, Union[tf.Tensor, tf.SparseTensor]]) -> Dict[str, tf.Tensor]:
    """tf.transform's callback function for preprocessing inputs.
    """
    outputs = {}

    image_features = tf.map_fn(
        lambda x: tf.io.decode_jpeg(x[0], channels=3),
        inputs[constants.IMAGE_KEY],
        dtype=tf.uint8
        )

    # image_features = tf.cast(image_features, tf.float32)
    image_features = tf.image.resize(image_features, [constants.HEIGHT, constants.WIDTH])
    image_features = tf.keras.applications.efficientnet.preprocess_input(image_features)

    outputs[_transformed_name(constants.IMAGE_KEY)] = image_features
    # TODO(b/157064428): Support label transformation for Keras.
    # Do not apply label transformation as it will result in wrong evaluation.
    outputs[_transformed_name(constants.LABEL_KEY)] = inputs[constants.LABEL_KEY]
    return outputs
 

def _image_augmentation(image_features):
    """Perform image augmentation on batches of images .
    
    Args:
        image_features: a batch of image features
    
    Returns:
        The augmented image features
    """
    batch_size = tf.shape(image_features)[0]
    image_features = tf.image.random_flip_left_right(image_features)
    image_features = tf.image.resize_with_crop_or_pad(image_features, constants.HEIGHT + 30, constants.WIDTH + 30)
    image_features = tf.image.random_crop(image_features, (batch_size, constants.HEIGHT, constants.WIDTH, 3))
    return image_features


def _data_augmentation(feature_dict):
    """Perform data augmentation on batches of data.
    
    Args:
        feature_dict: a dict containing features of samples
    
    Returns:
        The feature dict with augmented features
    """
    image_features = feature_dict[_transformed_name(constants.IMAGE_KEY)]
    image_features = _image_augmentation(image_features)
    feature_dict[_transformed_name(constants.IMAGE_KEY)] = image_features
    return feature_dict


def _input_fn(file_pattern: List[Text], 
              tf_transform_output: tft.TFTransformOutput, 
              batch_size: int = 8, 
              is_train: bool = False) -> tf.data.Dataset:
    """Generates features and label for tuning/training.

    Args:
        file_pattern: input tfrecord file pattern.
        tf_transform_output: A TFTransformOutput.
        batch_size: representing the number of consecutive elements of returned
                    dataset to combine in a single batch
        is_train: Whether the input dataset is train split or not

    Returns:
        A dataset that contains (features, indices) tuple where features is a
        dictionary of Tensors, and indices is a single Tensor of label indices.
    """
    transformed_feature_spec = (
        tf_transform_output.transformed_feature_spec().copy())

    dataset = tf.data.experimental.make_batched_features_dataset(
        file_pattern=file_pattern,
        batch_size=batch_size,
        features=transformed_feature_spec,
        reader=_gzip_reader_fn,
        label_key=_transformed_name(constants.LABEL_KEY))

    if is_train:
        dataset = dataset.map(lambda x, y: (_data_augmentation(x), y))

    return dataset


def get_model(fn_args) -> tf.keras.Model:
    """Creates a CNN Keras model based on transfer learning for classifying image data.

    Returns:
      A keras Model.
    """
    img_shape = (constants.HEIGHT, constants.WIDTH, 3)

    # Create the base model from the pre-trained model EfficientNetB3
    base_model = tf.keras.applications.EfficientNetB3(
        input_shape=img_shape,
        include_top=False,
        weights=constants.PRETRAINED_WEIGHTS,
    )
    
    base_model.trainable = False
    # base_model.summary()
    global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
      
      
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=img_shape, dtype=tf.float32),
        base_model,
        global_average_layer,
        tf.keras.layers.Dropout(0.15),
        tf.keras.layers.Dense(6, activation="softmax")
    ])

    model.compile(optimizer=tf.optimizers.RMSprop(lr=0.01),
        loss="sparse_categorical_crossentropy",
        metrics=["sparse_categorical_accuracy"])
    model.summary(print_fn=absl.logging.info)
    
    return model


def run_fn(fn_args: TrainerFnArgs):
    """Train the model based on given args.

    Args:
        fn_args: Holds args used to train the model as name/value pairs.
    """
    tf_transform_output = tft.TFTransformOutput(fn_args.transform_output)

    train_dataset = _input_fn(
        fn_args.train_files,
        tf_transform_output,
        constants.TRAIN_BATCH_SIZE,
        is_train=True
    )

    eval_dataset = _input_fn(
        fn_args.eval_files,
        tf_transform_output,
        constants.EVAL_BATCH_SIZE,
        is_train=False
    )

    # # check for availabe tpu and gpu units
    # try:
    #   tpu = tf.distribute.cluster_resolver.TPUClusterResolver()
    #   tf.config.experimental_connect_to_cluster(tpu)
    #   tf.tpu.experimental.initialize_tpu_system(tpu)
    #   strategy = tf.distribute.experimental.TPUStrategy(tpu)
    # except ValueError:
    #   strategy = tf.distribute.MirroredStrategy()

    # with strategy.scope():
    model = get_model(fn_args)

    try:
        log_dir = fn_args.model_run_dir
    except KeyError:
        log_dir = os.path.join(os.path.dirname(fn_args.serving_model_dir), "logs")

    absl.logging.info('Tensorboard logging to {}'.format(log_dir))

    callbacks = [
                #  tf.keras.callbacks.ModelCheckpoint("DeepLabV3plus.ckpt", verbose=1, save_weights_only=True, save_best_only=True),
                 tf.keras.callbacks.ReduceLROnPlateau(monitor="iou_score", factor=0.2, patience=6, verbose=1, mode="max"),
                 tf.keras.callbacks.EarlyStopping(monitor="iou_score", patience=16, mode="max", verbose=1, restore_best_weights=True),
                 tf.keras.callbacks.TensorBoard(log_dir=log_dir, update_freq="batch")
    ]

    absl.logging.info('Start training the top classifier')
    
    model.fit(
        train_dataset,
        epochs=constants.EPOCHS,
        steps_per_epoch=fn_args.train_steps,
        validation_data=eval_dataset,
        validation_steps=fn_args.eval_steps,
        callbacks=callbacks
    )

    signatures = {
        'serving_default':
            _get_serve_image_fn(model).get_concrete_function(
                tf.TensorSpec(
                    shape=[None, constants.HEIGHT, constants.WIDTH, 3],
                    dtype=tf.float32,
                    name=_transformed_name(constants.IMAGE_KEY)
                )
            )
    }

    model.save(fn_args.serving_model_dir, save_format='tf', signatures=signatures)