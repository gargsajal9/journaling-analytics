from flask import Flask, request, Response , jsonify
import json
from flask import render_template
import dashboard
import summary

app = Flask(__name__, static_folder='public', static_url_path='')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

dashboard.initDashboard()


@app.route('/')
def index():
	return render_template('index.jade')

@app.route('/getEvents')
def getEvents():
	return Response(json.dumps(dashboard.getEventsfromLog()),mimetype='application/json')

@app.route('/getState')
def getState():
	#return jsonify(dashboard.getState())
	return Response(json.dumps(dashboard.getState()),mimetype='application/json')

@app.route('/openFile/<filepath>')
def openFile(filepath):
	dashboard.openFile(filepath)
	return jsonify({'status':'success'})

@app.route('/openInBrowser/<filepath>')
def openInBrowser(filepath):
	dashboard.openInBrowser(filepath)
	return jsonify({'status':'success'})

@app.route('/addTag/<tag>/<filepath>')
def addTag(filepath,tag):
	dashboard.AddTag(filepath,tag)
	return jsonify({'status':'success'})

@app.route('/removeTag/<tag>/<filepath>')
def removeTag(filepath,tag):
	dashboard.RemoveTag(filepath,tag)
	return jsonify({'status':'success'})

@app.route('/addTagURL',methods=['POST'])
def addTagURL():
	dashboard.AddTagURL(request.form.get('url'),request.form.get('tag'))
	return jsonify({'status':'success'})

@app.route('/removeTagURL',methods=['POST'])
def removeTagURL():
	dashboard.RemoveTagURL(request.form.get('url'),request.form.get('tag'))
	return jsonify({'status':'success'})

@app.route('/clearTag/<tag>')
def clearTag(tag):
	dashboard.clearTag(tag)
	return jsonify({'status':'success'})

@app.route('/getUnity')
def getUnity():
	return dashboard.getUnity()	

@app.route('/openAll/<tag>')
def openAll(tag):
	ret = dashboard.openAll(tag)
	return jsonify(ret)

@app.route('/getAllTagsByFile',methods=['POST'])
def getAllTagsByFile():
	res=dashboard.getAllTagsByFile(request.form.get('filepath'))
	return jsonify({ 'status':'success','result':res})

@app.route('/uploadDocument',methods=['POST'])
def uploadDocument():
	dashboard.uploadDocument(request.form.get('filepath'),request.form.get('task'))
	return jsonify({'status':'success'})

@app.route('/getSummary',methods=['POST'])
def getSummary():
	return jsonify(summary.getSummary(request.form.get('filepath'),5))

if __name__ == '__main__':
    app.run()
