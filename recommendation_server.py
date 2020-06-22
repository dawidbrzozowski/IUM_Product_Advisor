from flask import Flask, request, jsonify, render_template

from preprocessing.web_app_preprocessing import SessionRecommendationPreprocessor
from recommenders.rankers import NNRecommendationGenerator

app = Flask(__name__)

srp = SessionRecommendationPreprocessor()
recommendation_generator = NNRecommendationGenerator()
products_representation = srp.create_product_representation_for_web_app()


def get_recommendation_for_user_nn(user_id):
    session = srp.preprocess_user(user_id)
    recommendations = recommendation_generator.get_generated_recommendations(session)
    recommendation_texts = []
    for recommendation in recommendations:
        recommendation_texts.append(str(recommendation))
    return recommendation_texts


def get_recommendation_for_products_nn(product_ids):
    session = srp.preprocess_products(product_ids)
    recommendations = recommendation_generator.get_generated_recommendations(session)
    recommendation_texts = []
    for recommendation in recommendations:
        recommendation_texts.append(str(recommendation))
    return recommendation_texts


def get_recommendation_for_user_baseline(user_id):
    pass


def get_recommendation_for_products_baseline(product_ids):
    pass


@app.route('/')
def home():
    return render_template('index.html', choices=products_representation)


@app.route('/predict_user_nn', methods=['POST'])
def predict_user_nn():
    '''
    For rendering results on HTML GUI
    '''
    user_id = request.form.get('user_id')
    recommendation_texts = get_recommendation_for_user_nn(user_id)

    print('[LOG INFO] prediction was made for user ', user_id)
    return render_template('index.html', choices=products_representation, prediction_text_nn=recommendation_texts)


@app.route('/predict_from_products_nn', methods=['POST'])
def predict_from_products_nn():
    '''
    For rendering results on HTML GUI
    '''
    products_repr = request.form.getlist('choices')
    product_ids = srp.web_app_product_representation_to_product_ids(products_repr)
    recommendation_texts = get_recommendation_for_products_nn(product_ids)
    print('[LOG INFO] prediction was made for product: ', products_repr)
    return render_template('index.html', choices=products_representation, prediction_text_nn=recommendation_texts)


@app.route('/predict_api_nn', methods=['POST'])
def predict_api_nn():
    '''
    For direct API calls trought request
    '''
    req = request.get_json()
    if 'user_id' in req:
        recommendations = get_recommendation_for_user_nn(req['user_id'])
    elif 'session_history' in req:
        recommendations = get_recommendation_for_products_nn(req['session_history'])
    else:
        recommendations = 'No valid data provided.'
    return jsonify(recommendations)


@app.route('/predict_user_baseline', methods=['POST'])
def predict_user_baseline():
    '''
    For rendering results on HTML GUI
    '''
    user_id = request.form.get('user_id')
    # todo wyznaczyc rekomendacje dla usera przez baseline

    print('[LOG INFO] prediction was made for user ', user_id)
    return render_template('index.html', choices=products_representation, prediction_text_base=recommendation_texts)


@app.route('/predict_from_products_baseline', methods=['POST'])
def predict_from_products_baseline():
    '''
    For rendering results on HTML GUI
    '''
    products_repr = request.form.getlist('choices')
    product_ids = srp.web_app_product_representation_to_product_ids(products_repr)

    # todo wyznaczyc rekomendacje dla historii produktow przez baseline
    print('[LOG INFO] prediction was made for product: ', products_repr)
    return render_template('index.html', choices=products_representation, prediction_text_base=recommendation_texts)


@app.route('/predict_api_baseline', methods=['POST'])
def predict_api_baseline():
    '''
    For direct API calls trought request
    '''
    req = request.get_json()
    if 'user_id' in req:
        pass # todo
    elif 'session_history' in req:
        pass # todo
    else:
        recommendations = 'No valid data provided.'
    return jsonify(recommendations)


if __name__ == "__main__":
    app.run()
