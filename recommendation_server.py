from flask import Flask, request, jsonify, render_template

from preprocessing.web_app_preprocessing import SessionRecommendationPreprocessor
from recommenders.rankers import NNRecommendationGenerator
from utils.files_io import load_json

app = Flask(__name__)

srp = SessionRecommendationPreprocessor()
recommendation_generator = NNRecommendationGenerator()
products_representation = srp.create_product_representation_for_web_app()

@app.route('/')
def home():
    return render_template('index.html', choices=products_representation)


@app.route('/predict_user', methods=['POST'])
def predict_user():
    '''
    For rendering results on HTML GUI
    '''
    x = request.form.get('user_id')
    return render_template('index.html', choices=products_representation, prediction_text=f'User{x}')


@app.route('/predict_session', methods=['POST'])
def predict_session():
    '''
    For rendering results on HTML GUI
    '''


@app.route('/predict_from_products', methods=['POST'])
def predict_from_products():
    '''
    For rendering results on HTML GUI
    '''
    products_repr = request.form.getlist('choices')
    product_ids = srp.web_app_product_representation_to_product_ids(products_repr)
    session = srp.preprocess(product_ids)
    recommendations = recommendation_generator.get_generated_recommendations(session)
    recommendation_texts = []
    for recommendation in recommendations:
        recommendation_texts.append(str(recommendation))
    return render_template('index.html', choices=products_representation, prediction_text=recommendation_texts)


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
