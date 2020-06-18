import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    x = request.form.get('user_id')
    return render_template('index.html', prediction_text=f'Employee Salary should be {x}')

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)

    output = 4
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)