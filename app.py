import os

from flask import Flask,render_template,request
from utils.run_model import getBaseMap


app=Flask(__name__)

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload",methods=['POST'])
def upload():
    target='./static'
    if not os.path.isdir(target):
        os.mkdir(target)

    else :
        # remove older images
        for fname in os.listdir(target):
            if fname.endswith('.jpg') or fname.endswith('.png'):
                os.remove(os.path.join(target, fname))

    for f in request.files.getlist("file"):
        filename="input.jpg"
        dest=os.path.join(target, filename)
        f.save(dest)

    # save basemap to static as output.png
    resp = getBaseMap()
    if type(resp) == str:
        return resp

    filename = "output.png"
    return render_template("complete.html" , image_name=filename)
    
if __name__=="__main__":
    app.run(debug=True)
