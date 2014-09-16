from flask import Flask, render_template
from flask.ext.script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def home():
	"""
	Test
	"""
	print "Loading home.html"
	return render_template('home.html')

if __name__ == '__main__':
	manager.run()
