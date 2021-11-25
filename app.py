# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 19:24:21 2021

@author: nilay
"""

from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

model = pickle.load(open('random_forest_regression.pkl', 'rb'))
@app.route('/',methods=['GET'])

def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route('/predict',methods=['POST'])

def predict():
    Fuel_Type_Diesel = 0
    Fuel_Type_Petrol = 0
    if request.method =='POST':
        Year = int(request.form['Year'])
        no_of_years = 2021 - Year
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        
        
        Fuel_Type = request.form['Fuel_Type']
        if(Fuel_Type == 'Petrol'):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif(Fuel_Type == 'Diesel'):
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0
        
        
        
        Seller_Type = request.form['Seller_Type']
        if(Seller_Type == 'Individual'):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        
        
        
        Transmission_Type = request.form['Transmission']
        if(Transmission_Type == 'Manual'):
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0
        prediction = model.predict([[Present_Price, Kms_Driven, Owner, no_of_years, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])
        output = round(prediction[0],2)
        
        if output<0:
            return render_template('index.html', prediction_text = "Sorry you can't sell this car!")
        else:
            return render_template('index.html', prediction_text = "You can sell this car at {} lakhs".format(output))
    
    
    else:
        return render_template('index.html')
    
    
if __name__ == "__main__":
    app.run(debug=True)