# Constant paths for saving inputs, weights
from unet.unet_baseline import *
from unet.loss_metrics import *

IMG_PATH = ""
OUTPUT_PATH = ""
BUILDING_WEIGHTS = ""
ROAD_WEIGHTS = ""
GREEN_WEIGHTS = ""
WATER_WEIGHTS = ""

BUILDING_COLOR = ""
ROAD_COLOR = ""
GREEN_COLOR = "green"
WATER_COLOR = "blue"

def retMask(img, weights_path):
	model = uNet()
	model.load_weights(weights_path)
	# YET TO IMPLEMENT


def splitImageAndTest(img, weights_path):
	Y = np.zeros((img.shape(0), img.shape(1), image.shape(2)), np.uint8)
	for i in range(0, img.shape(0), 256):
		for j in range(0, img.shape(1), 256):
			Y[i:i+255. j:j+255] = retMask(img[i:i+255, j:j+255], weights_path)

	return Y


def colourMask(mask, color):
	# YET TO DEFINE



def getMaps(opt):
	# check if input image is available
	if !os.path.exists(os.path.join(IMG_PATH, "*.jpg")):
		# -1 is image not found or error in input shape
		return -1
	
	img = Image.open(IMG_PATH)
	img = np.array(img)
	if(img.shape(0)%256 != 0 || img.shape(1)%256 != 0 || img.shape(2) != 3):
		return -1

	# Buildings
	if opt == 1:
		Y = splitImageAndTest(img, BUILDING_WEIGHTS)
		Y = colourMask(Y, BUILDING_COLOR)
		return Y

	# Roads
	if opt == 2:
		Y = splitImageAndTest(img, ROAD_WEIGHTS)
		Y = colourMask(Y, ROAD_COLOR)
		return Y

	# Greenery
	if opt == 3:
		Y = splitImageAndTest(img, GREEN_WEIGHTS)
		Y = colourMask(Y, GREEN_COLOR)
		return Y

	# Water
	if opt == 4:
		Y = splitImageAndTest(img, WATER_WEIGHTS)
		Y = colourMask(Y, WATER_COLOR)
		return Y


def mergeMaps(map1, map2):
	# YET TO DEFINE



def getBaseMap():
	Y = getMaps(4)
	Y = mergeMaps(Y, getMaps(3))
	Y = mergeMaps(Y, getMaps(2))
	Y = mergeMaps(Y, getMaps(1))

	Y = Image.fromarray(Y)
	Y.save(OUTPUT_PATH)
	return 0