from flask import Flask, redirect, url_for, request, render_template, make_response, send_file, Response
import requests

app = Flask(__name__)

@app.route('/download/<filename>')
def download_file(filename):
    try:
        # get_blob(filename)
        response = requests.get('http://dbapi-service-container:5004/read/'+filename)
        return "downloading"
    except:
        return "download failed. Please try again."  

if __name__ == '__main__':
#    app.run("127.0.0.1", port=5001)
   app.run(host='0.0.0.0', port=5002)        