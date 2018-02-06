#!flask/bin/python

import sys, Queue

from flask import Flask, Response, render_template, send_from_directory, url_for#, request, redirect

q = Queue.Queue()
for i in range(-5,5):
	q.put((float(i), float(i), float(i)))

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
		elem = q.get()
		return str(elem[0]) + "," + str(elem[1]) + "," + str(elem[2])

if __name__ == '__main__':
	app.run()

"""
- python server constantly gets the output coordinates from python script
- When JS GET on /server, the python server sends the last point in the queue

"""