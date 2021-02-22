# Constant paths for saving inputs, weights
from unet.unet_baseline import *
from unet.loss_metrics import *

IMG_PATH = "C:/Users/G Sudhamsu/Desktop/PROJECT DOC/app/Sat_Image_Seg/static"
OUTPUT_PATH = IMG_PATH

BUILDING_WEIGHTS = "C:/Users/G Sudhamsu/Desktop/PROJECT DOC/app/Sat_Image_Seg/weights/buildings/model_sample.h5"
ROAD_WEIGHTS = ""
GREEN_WEIGHTS = ""
WATER_WEIGHTS = ""

IMG_HEIGHT = IMG_WIDTH = 256
IMG_CHANNELS = 3

def retMask(img, weights_path):
	model = uNet()
	model.load_weights(weights_path)
	X_test = np.zeros((1, IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.float32)
	X_test[0] = img
	preds_test=model.predict(X_test, verbose=1)
	preds_test = (preds_test > 0.7).astype(np.uint8)
	mask=preds_test[0]
	for i in range(mask.shape[0]):
		for j in range(mask.shape[1]):
			if mask[i][j] == 1:
				mask[i][j] = 255
			else:
				mask[i][j] = 0

	merged_image = cv2.merge((mask,mask,mask))
	return merged_image


def splitImageAndTest(img, weights_path):
	Y = np.zeros((img.shape[0], img.shape[1], img.shape[2]), np.uint8)
	for i in range(0, img.shape[0], 256):
		for j in range(0, img.shape[1], 256):
			Y[i:i+256, j:j+256] = retMask(img[i:i+256, j:j+256], weights_path)

	return Y


def colourMask(opt):
	# YET TO DEFINE
	if opt == 1: colour = [255, 0, 0] # RED
	if opt == 2: colour = [0, 0, 0]   # BLACK
	if opt == 3: colour = [0, 255, 0] # GREEN
	if opt == 4: colour = [0, 0, 255] # BLUE

	file_path = os.path.join(OUTPUT_PATH, "{}_mask.jpg".format(opt))
	if not os.path.exists(file_path):
		return "No mask found to colour!"

	image = plt.imread(file_path)
	image_copy = image.copy() #image is read only, therefore copy
	
	black_pixels_mask = np.all(image == [0, 0, 0], axis=-1)
	non_black_pixels_mask = np.any(image != [0, 0, 0], axis=-1) 
	
	image_copy[black_pixels_mask] = [255, 255, 255]
	image_copy[non_black_pixels_mask] = colour

	plt.imsave(os.path.join(OUTPUT_PATH, '{}_color.png'.format(opt)), image_copy)


def segmentMaps(opt):
	# check if input image is available
	file_path = os.path.join(IMG_PATH, "input.jpg")
	if not os.path.exists(file_path):
		# -1 is image not found or error in input shape
		return "Image Not found!"
	
	img = Image.open(file_path, 'r')
	img = np.array(img)
	if(img.shape[0]%256 != 0 or img.shape[1]%256 != 0 or img.shape[2] != 3):
		return "Image size invalid"

	# Segmentation
	# Buildings
	if opt == 1:
		Y = splitImageAndTest(img, BUILDING_WEIGHTS)

	# Roads
	if opt == 2:
		Y = splitImageAndTest(img, ROAD_WEIGHTS)

	# Greenery
	if opt == 3:
		Y = splitImageAndTest(img, GREEN_WEIGHTS)

	# Water
	if opt == 4:
		Y = splitImageAndTest(img, WATER_WEIGHTS)

	if type(Y) == str:
		return Y
	
	Y = Image.fromarray(Y)
	Y.save(os.path.join(OUTPUT_PATH, '{}_mask.jpg'.format(opt)), 'JPEG')
	return 0


#def mergeMaps(map1, map2):
	# YET TO DEFINE


def getBaseMap():
	for i in range(1, 1+1):
		Y = segmentMaps(i)

		if type(Y) == str:
			return Y

		Y = colourMask(i)

		if type(Y) == str:
			return Y
	
	#Y = mergeMaps()
	#Y = Image.fromarray(Y)
	#Y.save(os.path.join(OUTPUT_PATH, 'output.jpg'), 'JPEG')
	return 0