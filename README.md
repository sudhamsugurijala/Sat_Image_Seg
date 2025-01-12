# Satellite Image Segmentation
* Generates base maps of regions by performing image segmentation on satellite images.
* These base maps can be used for performing topological analysis.
  * For example - estimate the topological changes post a natural disaster. 

## How To Run
* Install requirements from text file
* `app.py` is the entry point
* `templates` contains HTML files
* `static` contains pictures, CSS, JS files

In root dir (same level as `app.py`) -
* Create a `weights` folder with sub folders for each class of segmentation targets (like `road`, `building`, `water` etc).
* Store weights in respective subfolders.

## Sample User Flow
* The user uploads an image from their local file system
* A preview of the input image is shown


![loading input](https://github.com/sudhamsugurijala/Satellite-Image-Segmentation/blob/main/static/css/images/input.png)


* After the user clicks the `Upload Image` button, the app processes the input image and generates the result as shown below:


![result page](https://github.com/sudhamsugurijala/Satellite-Image-Segmentation/blob/main/static/css/images/result.png)


* The user can click the `Validate Map` button to superimpose the result on the input image as shwon below:

![validating result](https://github.com/sudhamsugurijala/Satellite-Image-Segmentation/blob/main/static/css/images/validation.png)


## Publication
* This work is published in the following chapter - [Link](https://link.springer.com/chapter/10.1007/978-3-031-05767-0_27)
  * It was also presented at the conference mentioned in the chapter.
