
IMAGE_KEY = "image_raw"
MASK_KEY = "mask_raw"

EPOCHS = 1
TRAIN_STEPS = 1
EVAL_STEPS = 2
TRAIN_BATCH_SIZE = 4
EVAL_BATCH_SIZE = 1
HEIGHT = 320
WIDTH = 320
PRETRAINED_WEIGHTS = "imagenet"
BACKBONE_TRAINABLE = False
BACKBONE_NAME = "efficientnetb3"

TOTAL_CLASSES = ['sky', 'building', 'pole', 'road', 'pavement', 
               'tree', 'signsymbol', 'fence', 'car', 
               'pedestrian', 'bicyclist', 'unlabelled']
N_TOTAL_CLASSES = 12
MODEL_CLASSES = ["sky", "building"]
if len(MODEL_CLASSES) == 11:
    ALL_CLASSES = True
    MODEL_CLASSES = TOTAL_CLASSES
    N_MODEL_CLASSES = N_TOTAL_CLASSES
else:
    ALL_CLASSES = False
    N_MODEL_CLASSES = len(MODEL_CLASSES) + 1