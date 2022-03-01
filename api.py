from flask import Flask, request
from flask_restful import Resource, Api
import sys
import settings


class UnicodeApi(Api):
	def __init__(self, *args, **kwargs):
		super(UnicodeApi, self).__init__(*args, **kwargs)
		self.app.config['RESTFUL_JSON'] = {
			'ensure_ascii': False
		}
		self.representations = {
			'application/json; charset=utf-8': output_json,
		}

app = Flask(__name__)
api = UnicodeApi(app)

class Home(Resource):
	def get(self):
		return "done"

class CalculTempsParcours(Resource):
	def get(self,autonomyStr,chargeTimeStr,kmsStr,averageSpeedStr):
		autonomy = int(autonomyStr) # km
		chargeTime = int(chargeTimeStr) # min
		kms = int(kmsStr) # km
		averageSpeed = int(averageSpeedStr)/60.0 # km/min
		# t = d/v
		time = 0
		kmsLast = kms
		while(autonomy<kmsLast):
			time += chargeTime
			kmsLast -= autonomy
		time += kms/averageSpeed
		timeApproch = int(round(time,0))
		res = "À peu près "
		heures = int(timeApproch/60)
		if(heures > 0):
			res+=str(heures)+"h"
		minutes = int(timeApproch%60)
		if(minutes > 0):
			res +=str(minutes)+"min"
		return res


api.add_resource(Home, "/")
api.add_resource(CalculTempsParcours, "/Time/<autonomyStr>/<chargeTimeStr>/<kmsStr>/<averageSpeedStr>")

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	app.run(debug=True)

"""
[
    {
        "brand": "Renault",
        "model": "Zoé",
        "autonomy": 300,
        "chargeTime": 70
    }
]

[herokuApp]/Time/Renault/Zoé/300/70
"""