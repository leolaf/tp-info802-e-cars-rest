from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

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
		res = "A peu pres "
		if(timeApproch >= 60):
			heures = int(timeApproch/60)
			minutes = int(timeApproch%60)
		res+=str(heures)+"h"+str(minutes)+"min"
		return res


api.add_resource(CalculTempsParcours, "/Time/<autonomyStr>/<chargeTimeStr>/<kmsStr>/<averageSpeedStr>")

if __name__ == "__main__":
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