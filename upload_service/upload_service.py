from flask import Flask, redirect, url_for, request, render_template, make_response, send_file, Response
# from flask_api import status
from werkzeug.utils import secure_filename
import requests

app = Flask(__name__)

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file2():
   if request.method == 'POST':
    try:
        f = request.files['file']
        # f.save(secure_filename(f.filename)) ## delete after using it
        # insert_blob(filename=f.filename)
        response = requests.post('http://dbapi-service-container:5004/write', 
                files = {'file': f})
                # files = {'file': open('myfirstreact.png' ,'rb')})

        return 'file uploaded successfully'
    except:
        return 'file not uploaded. Please try again.'   

if __name__ == '__main__':
#    app.run("127.0.0.1", port=5001)
   app.run(host='0.0.0.0', port=5001)        