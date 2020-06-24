# IUM Product Recommendation

### Install all needed packages by using: pip install -r requirements.txt

<br><br>

## Introduction

The application is a Web App used for generating product recommendation lists based on
either user id or a collection of products. 
The app allows to compare recommendation from:
- neural network
- collaborative filtering

<br><br>

## Usage of application ###
Run the application server using:
```
python -m recommendation_server .
```

This will launch the demonstration web application and allow you to send queries using POST request.
Web app is going to launch on:
```
http://127.0.0.1:5000
```

<br><br>

## Getting prediction from terminal
#### Send a post request to the server by using i.e. requests API. <br>

Send a request for a given user and specified model: <br>
for collaborative:

```
request = requests.post("http://127.0.0.1:5000/predict_api_baseline", json={'user_id': any_user_id)
```

for neural network:
```
request = requests.post("http://127.0.0.1:5000/predict_api_nn", json={'user_id': any_user_id) 
```

######
Send a request for a session of products


for collaborative:
```
request = requests.post("http://127.0.0.1:5000/predict_api_baseline", json={'session_history': [list_of_product_ids]})
```
for neural network:
```
request = requests.post("http://127.0.0.1:5000/predict_api_nn", json={'session_history': [list_of_product_ids]})
```

<br><br>

## Getting prediction from GUI
From the web app there are many choices for prediction: <br>

- Selecting the user for whom the prediction will be generated. <br>
- Selecting a list of products that will act as a user session for which we will generate a prediction

Both of those methods are prepared for baseline and NN solution.
