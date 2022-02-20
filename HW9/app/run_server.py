import json

import dill
import pandas as pd
import os

dill._dill._reverse_typemap['ClassType'] = type

import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def load_model(model_path):
    # load the pre-trained model
    global model
    with open(model_path, 'rb') as f:
        model = dill.load(f)
    print(model)


modelpath = "/app/app/models/stars_pipeline.dill"
load_model(modelpath)


@app.route("/", methods=["GET"])
def general():
    return """Welcome to fraudelent prediction process. Please use 'http://<address>/predict' to POST"""


@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}
    dt = strftime("[%Y-%b-%d %H:%M:%S]")
    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":

        temperature, luminosity, radius, absolute_magnitude = 0.0, 0.0, 0.0, 0.0
        star_color, spectral_class = "", ""

        request_json = flask.request.get_json()

        if request_json["temperature"]:
            temperature = float(request_json['temperature'])

        if request_json["luminosity"]:
            luminosity = float(request_json['luminosity'])

        if request_json["radius"]:
            radius = float(request_json['radius'])

        if request_json["absolute_magnitude"]:
            absolute_magnitude = float(request_json['absolute_magnitude'])

        if request_json["star_color"]:
            star_color = str(request_json['star_color'])

        if request_json["spectral_class"]:
            spectral_class = str(request_json['spectral_class'])

        logger.info(f'{dt} Data: temperature={temperature}, '
                    f'luminosity={luminosity}, '
                    f'radius={radius}'
                    f'absolute_magnitude={absolute_magnitude}'
                    f'star_color={star_color}'
                    f'spectral_class={spectral_class}'
                    )

        try:
            preds = model.predict_proba(pd.DataFrame(
                {
                    "Temperature (K)": [temperature],
                    "Luminosity(L/Lo)": [luminosity],
                    "Radius(R/Ro)": [radius],
                    "Absolute magnitude(Mv)": [absolute_magnitude],
                    "Star color": [star_color],
                    "Spectral Class": [spectral_class]
                }
            ))
        except AttributeError as e:
            logger.warning(f'{dt} Exception: {str(e)}')
            data['predictions'] = str(e)
            data['success'] = False
            return flask.jsonify(data)

        data["predictions"] = preds[0].tolist()
        # indicate that the request was a success
        data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)


if __name__ == "__main__":
    print(("* Loading the model and Flask starting server..."
           "please wait until server has fully started"))
    port = int(os.environ.get('PORT', 8180))
    app.run(host='0.0.0.0', debug=True, port=port)
