import os
from unet.unet_baseline import *
from flask import Flask,render_template,request

app=Flask(__name__)
APP_ROOT=os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload",methods=['POST'])
def upload():
    target=os.path.join(APP_ROOT,'static/')
    if not os.path.isdir(target):
        os.mkdir(target)
    for f in request.files.getlist("file"):
        filename=f.filename
        dest="/".join([target,filename])
        f.save(dest)
    return render_template("complete.html" , image_name=filename)
    
if __name__=="__main__":
    app.run()
