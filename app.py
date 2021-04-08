import os
import uuid

from flask import Flask,render_template,request, make_response
from utils.run_model import getBaseMap

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("upload.html")


@app.route('/loading', methods=['POST'])
def loading():
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

    return render_template('loading.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method=='GET':
        filename = None
        # file used for storing base map name between requests
        with open("./static/filename.txt", 'r') as f:
            filename = f.read()
        return render_template("complete.html" , image_name=filename)

    if request.method=='POST':
        # save basemap to static as map_token.png
        # token is a 6 digit unique id for each map output (browser cache solution)
        token = uuid.uuid4().hex[:6] 
        resp = getBaseMap(token)
        if type(resp) == str:
            return resp

        filename = "map_{}.png".format(token)
        # file used for storing base map name between requests
        with open("./static/filename.txt", 'w') as f:
            f.write(filename)
        return make_response('POST request successful', 200)
    
if __name__=="__main__":
    app.run(debug=True)
