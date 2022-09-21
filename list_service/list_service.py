from flask import Flask, redirect, url_for, request, render_template, make_response, send_file, Response
import requests

app = Flask(__name__)

@app.route('/list')
def show_all():
    # data = read_table()
    data = requests.get('http://dbapi-service-container:5004/list')
    return render_template('list.html', result = data.json())


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5003)        