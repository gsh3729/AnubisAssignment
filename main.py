from ast import If
from flask import Flask, redirect, url_for, request, render_template, make_response
from werkzeug.utils import secure_filename
from mysql.connector import MySQLConnection, Error

app = Flask(__name__)

def read_file(filename):
    with open(filename, 'rb') as f:
        fileContent = f.read()
    return fileContent

def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)    

def read_db_config():
    db = {}
    db['host'] = "127.0.0.1"
    db['database'] = "filesdb"
    db['user'] = "root"
    db['password'] = "12121212"
    return db

def insert_blob(filename, data = None):
    if data == None:
        print("Reading as data is empty")
        data = read_file(filename)
    query = "INSERT INTO file_table (filename, file) VALUES (%s , %s)"
    args = (filename, data)
    db_config = read_db_config()
    try:
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as e:
        print("Error: ", e)
    finally:
        cursor.close()
        conn.close()

def read_table():
    query = "SELECT id, filename FROM file_table"
    db_config = read_db_config()
    res = {}
    try:
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.commit()
        print("Length: ", len(data))
        for i in data:
            res[i[0]] = i[1]
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close() 
    return res    


def get_blob(filename):
    query = "SELECT * FROM file_table WHERE filename = %s"
    db_config = read_db_config()
    try:
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, (filename,))
        data = cursor.fetchone()
        print("Length: ", len(data))
        write_file(data[2], filename)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()        

@app.route('/download/<filename>')
def download_file(filename):
    try:
        get_blob(filename)
        return "downloading"
    except:
        return "download failed. Please try again."

@app.route('/list')
def show_all():
    data = read_table()
    return render_template('list.html', result = data)

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file2():
   if request.method == 'POST':
    try:
        f = request.files['file']
        f.save(secure_filename(f.filename)) ## delete after using it
        insert_blob(filename=f.filename)
        return 'file uploaded successfully'
    except:
        return 'file not uploaded. Please try again.'

@app.route('/harsha')
def hello_world():
   return "Hello harsha"		   

if __name__ == '__main__':
#    app.run("127.0.0.1", port=5001)
   app.run(host='0.0.0.0', port=80)