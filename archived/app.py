import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import re

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save_the_kids',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [float(x) for x in request.form.values()]

    if(int_features[0]<1 or int_features[0]>3):
        return render_template('index.html', prediction_text='Please enter a valid difficulty between 1 and 3')

    if(int_features[1]<0 or int_features[1]>7):
        return render_template('index.html', prediction_text='Please enter a valid workload between 0 and 7')

    if(int_features[2]<1 or int_features[2]>31):
        return render_template('index.html', prediction_text='Please enter a valid date between 1 and 31')    

    final_features = [np.array(int_features[0:2:1])]
    prediction = model.predict(final_features)
    date=int_features[2]
    output = round(prediction[0], 0)+date

    return render_template('index.html', prediction_text='The due date should be  {}'.format(output))

@app.route('/Assignments_bruh',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)