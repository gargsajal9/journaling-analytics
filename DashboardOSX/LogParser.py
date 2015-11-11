import json

def parse(line):
	if len(line)==0:
		return False
	try:
		#fields = line.split()
		res={}
		#res['date']=fields[0]
		#res['time']=fields[1]
		if "JSON:" in line:
			res["json"]=line[line.index('{'):]
			res["type"]="event"
		else:
			res["message"]=fields[3]
			res["type"]="log"
		#return res
		return json.loads(res["json"])["content"]
	except:
		return False