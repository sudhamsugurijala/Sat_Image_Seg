from unet.unet_baseline import *
from unet.loss_metrics import *

IMG_HEIGHT = IMG_WIDTH = 256
IMG_CHANNELS = 3

def retMask(img, weights_path):
	"""Return mask given image aand weights path"""
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
