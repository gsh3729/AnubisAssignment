from flask import Flask, redirect, url_for, request, render_template, make_response, send_file, Response
# from flask_api import status
from werkzeug.utils import secure_filename
from mysql.connector import MySQLConnection, Error, pooling

import threading
import concurrent.futures

app = Flask(__name__)
connection_pool = pooling.MySQLConnectionPool(pool_name="my_pool",
                                                  pool_size=5,
                                                  pool_reset_session=True,
                                                  host="db-container",
                                                  database="filesdb",
                                                  user="root",
                                                  password="root")

# def read_db_config():
#     db = {}
#     db['host'] = "db-container"
#     db['database'] = "filesdb"
#     db['user'] = "root"
#     db['password'] = "root"
#     return db

# connection_pool = pooling.MySQLConnectionPool(**read_db_config())

rd = threading.Semaphore()  #initializing semaphores using Semaphore class in threading module for reading and wrting
wrt = threading.Semaphore()  

readCount = 0   #initializing number of reader present

def reader(self):
    while True:
        rd.acquire()      #wait on read semaphore 

        self.readCount+=1       #increase count for reader by 1

        if readCount == 1: #since reader is present, prevent writing on data
            wrt.acquire() #wait on write semaphore

        rd.release()     #signal on read semaphore

        print(f"Reader {self.readCount} is reading")

        rd.acquire()   #wait on read semaphore 

        readCount-=1   #reading performed by reader hence decrementing readercount

        if readCount == 0: #if no reader is present allow writer to write the data
            wrt.release()  # signal on write semphore, now writer can write

        rd.release()      #sinal on read semaphore
        # time.sleep(3)   
    return       

def writer():
    while True:
        wrt.acquire()     #wait on write semaphore

        print("Wrting data.....")  # write the data
        print("-"*20)

        wrt.release()      #sinal on write semaphore
        # time.sleep(3)    
    return  

# def main(self):
#     # calling mutliple readers and writers
#     t1 = threading.Thread(target = self.reader) 
#     t1.start()
#     t2 = threading.Thread(target = self.writer) 
#     t2.start()
#     t3 = threading.Thread(target = self.reader) 
#     t3.start()
#     t4 = threading.Thread(target = self.reader) 
#     t4.start()
#     t6 = threading.Thread(target = self.writer) 
#     t6.start()
#     t5 = threading.Thread(target = self.reader) 
#     t5.start()

def read_file(filename):
    with open(filename, 'rb') as f:
        fileContent = f.read()
    return fileContent

def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)    

        



def reading_fromtable(filename):
    query = "SELECT * FROM file_table WHERE filename = %s"
    try:
        conn = connection_pool.get_connection()
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query, (filename,))
            data = cursor.fetchone()
            print("Length: ", len(data))
            write_file(data[2], filename)
    except Error as e:
        print(e)
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()    

    return True    

def writing_totable(filename, data = None):
    if data == None:
        data = read_file(filename)
    query = "INSERT INTO file_table (filename, file) VALUES (%s , %s)"
    args = (filename, data)
    try:
        conn = connection_pool.get_connection()
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query, args)
            conn.commit()
    except Error as e:
        print("Error: ", e)
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()  
    return True     

def read_fulltable():
    query = "SELECT id, filename FROM file_table"
    res = {}
    try:
        conn = connection_pool.get_connection()
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            print("Length: ", len(data))
            for i in data:
                res[i[0]] = i[1]
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close() 
    return res         

@app.route('/read/<filename>')
def read_endpoint(filename):
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(reading_fromtable, filename)
            return_value = future.result()
        if return_value:  
            return send_file(filename)
        else:
            return Response("Record not found", status=400)
    except:
        return Response("Server internal error", status=500)        



@app.route('/write', methods = ['POST'])
def write_endpoint():
    try:
        if request.method == 'POST':
            f = request.files['file']
            f.save(secure_filename(f.filename)) ## delete after using it
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(writing_totable, f.filename)
                return_value = future.result()
            if return_value:  
                return Response("Write operation done", status=200)
            else:
                return Response("Write operation failed", status=400)
    except:
        return Response("Server internal error", status=500)     

@app.route('/list')
def list_endpoint():
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(read_fulltable)
            return_value = future.result()
        if return_value:  
            return return_value
        else:
            return Response("Record not found", status=400)
    except:
        return Response("Server internal error", status=500)   
    
if __name__=="__main__":
    app.run(host='0.0.0.0', port=5004)
    # c = ReaderWriter()
    # c.main()    
