from flask import Flask, redirect, url_for, request, render_template, make_response, send_file, Response
# from flask_api import status
from werkzeug.utils import secure_filename
import requests

app = Flask(__name__)

@app.route('/')
def upload_service():
    return 'Hello, I am upload service!'

@app.route('/ping')
def do_ping():
    response = ''
    try:
        response = requests.get('http://download-service-container:5002/pong')
    except requests.exceptions.RequestException as e:
        print('\n Cannot reach the pong service.')
        return 'Ping ...\n'

    return 'Ping ... ' + response.text + ' \n'

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file2():
   if request.method == 'POST':
    try:
        f = request.files['file']
        f.save(secure_filename(f.filename)) 
        response = requests.post('http://dbapi-service-container:5004/write', 
                files = {'file': open(f.filename ,'rb')})

        return 'file uploaded successfully'
    except:
        return 'file not uploaded. Please try again.'   

if __name__ == '__main__':
#    app.run("127.0.0.1", port=5001)
   app.run(host='0.0.0.0', port=5001)        