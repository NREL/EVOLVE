# Standard imports
import json
import pickle
import os

# Third-party imports
from flask import Flask, request
from flask_cors import CORS

# Internal imports
from server.apidata import APIData
from server.profileapi import ProfileAPI
from note_global.data_handler_new import DataHandler

with open('/evolve/data/setting.json', "r") as infile:
    data_config = json.load(infile)

data_handler_instance = DataHandler(data_config)

app = Flask(__name__)
CORS(app)


@app.route('/getdata',methods=["POST"])
def get_data():

    api_instance = APIData(request.json, data_handler_instance )
    data = api_instance.get_data()
    return data

@app.route('/getfeeders',methods=["GET"])
def get_feeders():
    feeders = data_handler_instance.dt_metadata['Feeder Name'].tolist()
    return {'feeders': list(set(feeders)) }
    

@app.route('/gettransformers',methods=["GET"])
def get_transformers():

    transformers = data_handler_instance.dt_metadata['Transformer Name'].tolist()
    return {'transformers': list(set(transformers)) }

@app.route('/get_profile_data',methods=["POST"])
def get_profile():

    if hasattr(data_handler_instance, 'profile_instance'):
        api_instance = ProfileAPI(request.json, data_handler_instance.profile_instance)
        return api_instance.get_data()
    
    else:
        return {}


if __name__ == '__main__':
    app.run(debug=True)
