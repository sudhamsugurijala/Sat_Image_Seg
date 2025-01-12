# Sat_Image_Seg
Generates base maps for regions by performing image segmentation on satellite images.

## How To Run
* Install requirements from text file
* `app.py` is the entry point
* `templates` contains HTML files
* `static` contains pictures, CSS, JS files

In root dir (same level as `app.py`) -
* Create a `weights` folder with sub folders for each class of segmentation targets (like `road`, `building`, `water` etc).
* Store weights in respective subfolders.
