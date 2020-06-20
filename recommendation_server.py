from flask import Flask, request, jsonify, render_template

from preprocessing.web_app_preprocessing import SessionRecommendationPreprocessor
from recommenders.rankers import NNRecommendationGenerator

app = Flask(__name__)

srp = SessionRecommendationPreprocessor()
recommendation_generator = NNRecommendationGenerator()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict_user', methods=['POST'])
def predict_user():
    '''
    For rendering results on HTML GUI
    '''
    x = request.form.get('user_id')
    return render_template('index.html', prediction_text=f'User{x}')


@app.route('/predict_session', methods=['POST'])
def predict_session():
    '''
    For rendering results on HTML GUI
    '''
    x = request.form.values()
    x = list(x)
    session = srp.preprocess(x)
    recommendations = recommendation_generator.get_generated_recommendations(session)
    recommendation_text = ''
    for recommendation in recommendations:
        recommendation_text += str(recommendation)
        print(recommendation)
    return render_template('index.html', prediction_text=recommendation_text)


@app.route('/predict_api', methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)

    output = 4
    return jsonify(output)


if __name__ == "__main__":
    app.run()
