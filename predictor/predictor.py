from flask import Flask,render_template,request,url_for
import pickle
import os
import numpy as np

app = Flask(__name__)
MODELS = []
@app.route("/")
def index():
	#for i in range(6):
	#	filename = "var/www/html/predictor"+"/model/model"+str(i+1)+".pkl"
         #       #filename = os.path.join(os.getcwd(), "/model/model"+str(i+1)+".pkl")
          #      MODELS.append(pickle.load(open(filename, 'rb')))
	return render_template("index.html")

def isvalid(sample):
	temp = sample.split(',')
	data = []
	for element in temp:
		try:
    			data.append(float(element))
		except ValueError:
   			 return (False,[])
	if(len(data)!=200):
		return (False,[])
	data = np.array([data])
	#data = data.reshape(-1, 1)
	return (True, data)

@app.route("/",methods=["GET"])
def generate():
	if request.method == 'GET':
		return render_template('results.html')

@app.route("/",methods=['POST'])
def predict():
	comment = request.form["comment"]
	if request.method == 'POST':
		#print (comment)
		valid, data = isvalid(comment)
		if(not valid):
			return "Invalid Input"
			#return render_template('results.html',prediction = 3,comment = comment)
		else:
			counter = 0
			models = []
			models.append(request.form.getlist("CatBoost"))
              	 	models.append(request.form.getlist("NaiveBayes"))
                	models.append(request.form.getlist("DecisionTree"))
                	models.append(request.form.getlist("RandomForest"))
             	 	models.append(request.form.getlist("SVM"))
			models.append(request.form.getlist("LogReg"))
			results = []
			#return models
			for i in range(len(models)):
				if(models[i]):
					counter +=1 
					filename = "var/www/html/predictor"+"/model/model"+str(i+1)+".pkl"	
					#filename = os.path.join(os.getcwd(), "/model/model"+str(i+1)+".pkl")
					model = pickle.load(open(filename, 'rb'))
					results.append(model.predict(data))

				else:
					results.append(-1)
			#return str(results)
			return render_template('results.html',predict1=results[0], predict2=results[1],predict3=results[2],
							predict4=results[3],predict5=results[4],predict6=results[5])
if __name__ == '__main__':
	app.run()
