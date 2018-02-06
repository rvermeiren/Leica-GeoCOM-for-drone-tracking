#!flask/bin/python    

import sys, time, threading, Queue

from flask import Flask, Response, render_template, send_from_directory, url_for#, request, redirect

q = Queue.Queue()

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
        	time.sleep(0.1)
        	continue
        yield line

def read_data_file(file):
	datafile = open(file, "r")
	lines = follow(datafile)
	for line in lines:
		print("Adding point in queue")
		q.put(line, True)

app = Flask(__name__)

# Render html file
@app.route('/')
def output():
	return render_template('plot3d.html')

# Get icon
@app.route("/favicon.ico")
def favicon():
    app.add_url_rule('/favicon.ico',
                 redirect_to=url_for('static', filename='favicon.ico'))

# Upon request, send the next point in the queue
@app.route('/server')
def send_data():
	if q.empty():
		return Response("No data available", 204)
	else:
		elem = q.get(True)
		return elem

if __name__ == '__main__':
	t_read = threading.Thread(target=read_data_file, args = ('msg.txt',))
	t_read.start()
	app.run()