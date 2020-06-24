from flask import Flask, request, jsonify, render_template

from preprocessing.web_app_preprocessing import SessionRecommendationPreprocessor
from recommenders.rankers import NNRecommendationGenerator, CollaborativeRecommendationGenerator
from utils.files_io import load_json

app = Flask(__name__)

srp = SessionRecommendationPreprocessor()
recommendation_generator_nn = NNRecommendationGenerator()
recommendation_generator_baseline = CollaborativeRecommendationGenerator()
products_representation = srp.create_product_representation_for_web_app()


def get_recommendation_for_user(user_id, recommendation_generator):
    session = srp.preprocess_user(user_id)
    recommendations = recommendation_generator.get_generated_recommendations(session)
    recommendation_texts = []
    for recommendation in recommendations:
        print(type(recommendation_generator), recommendation)
        recommendation_texts.append(str(recommendation))
    return recommendation_texts


def get_recommendation_for_products(product_ids, recommendation_generator):
    session = srp.preprocess_products(product_ids)
    recommendations = recommendation_generator.get_generated_recommendations(session)
    recommendation_texts = []
    for recommendation in recommendations:
        recommendation_texts.append(str(recommendation))
    return recommendation_texts


@app.route('/')
def home():
    return render_template('index.html', choices=products_representation)


@app.route('/predict_user_nn', methods=['POST'])
def predict_user_nn():
    '''
    For rendering results on HTML GUI
    '''
    user_id = request.form.get('user_id')
    recommendation_texts = get_recommendation_for_user(user_id, recommendation_generator_nn)

    print('[LOG INFO] prediction was made for user ', user_id)
    return render_template('index.html', choices=products_representation, prediction_text_nn=recommendation_texts)


@app.route('/predict_from_products_nn', methods=['POST'])
def predict_from_products_nn():
    '''
    For rendering results on HTML GUI
    '''
    products_repr = request.form.getlist('choices')
    product_ids = srp.web_app_product_representation_to_product_ids(products_repr)
    recommendation_texts = get_recommendation_for_products(product_ids, recommendation_generator_nn)
    print('[LOG INFO] prediction was made for product: ', products_repr)
    return render_template('index.html', choices=products_representation, prediction_text_nn=recommendation_texts)


@app.route('/predict_api_nn', methods=['POST'])
def predict_api_nn():
    '''
    For direct API calls trought request
    '''
    req = request.get_json()
    if 'user_id' in req:
        recommendations = get_recommendation_for_user(req['user_id'], recommendation_generator_nn)
    elif 'session_history' in req:
        recommendations = get_recommendation_for_products(req['session_history'], recommendation_generator_nn)
    else:
        recommendations = 'No valid data provided.'
    return jsonify(recommendations)


@app.route('/predict_user_baseline', methods=['POST'])
def predict_user_baseline():
    '''
    For rendering results on HTML GUI
    '''
    user_id = request.form.get('user_id')
    print('wyznaczam dla', user_id)
    recommendation_texts = get_recommendation_for_user(user_id, recommendation_generator_baseline)
    print('[LOG INFO] prediction was made for user ', user_id)
    return render_template('index.html', choices=products_representation, prediction_text_base=recommendation_texts)


@app.route('/predict_from_products_baseline', methods=['POST'])
def predict_from_products_baseline():
    '''
    For rendering results on HTML GUI
    '''
    products_repr = request.form.getlist('choices')
    product_ids = srp.web_app_product_representation_to_product_ids(products_repr)
    recommendation_texts = get_recommendation_for_products(product_ids, recommendation_generator_baseline)
    print('[LOG INFO] prediction was made for product: ', products_repr)
    return render_template('index.html', choices=products_representation, prediction_text_base=recommendation_texts)


@app.route('/predict_api_baseline', methods=['POST'])
def predict_api_baseline():
    '''
    For direct API calls trought request
    '''
    req = request.get_json()
    if 'user_id' in req:
        recommendations = get_recommendation_for_user(req['user_id'], recommendation_generator_baseline)
    elif 'session_history' in req:
        recommendations = get_recommendation_for_products(req['session_history'], recommendation_generator_baseline)
    else:
        recommendations = 'No valid data provided'
    return jsonify(recommendations)


if __name__ == "__main__":
    app.run()
