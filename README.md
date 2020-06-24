# IUM Product Recommendation

### Install all needed packages by using: pip install -r requirements.txt
***
### Usage of application ###
- Run the application server using python -m recommendation_server .
<br>
This will launch the demonstration web application and allow you to send queries using POST request.
<br>
Web app is going to launch on: http://127.0.0.1:5000
<br>
<br>
- Send a post request to the server by using i.e. requests API.
<br>
Send a request for a given user: <br>
<i>request = requests.post("http://127.0.0.1:5000/predict_api_nn", json={'user_id': any_user_id)
</i><br>
Send a request for a session of products
<i>request = requests.post("http://127.0.0.1:5000/predict_api_nn", json={'session_history': [list_of_product_ids]})
</i>

- These requests may also be used for baseline if sent to the url: http://127.0.0.1:5000/predict_api_baseline 
***
- From the web app there are many choices for prediction: <br>
Selecting the user for whom the prediction will be generated. <br>
Selecting a list of products that will act as a user session for which we will generate a prediction

- Both of those methods are prepared for baseline and NN solution.
