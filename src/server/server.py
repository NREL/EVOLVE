# Standard imports
import json
import pickle
import os

# Third-party imports
from flask import Flask, request
from flask_cors import CORS

# Internal imports
from apidata import APIData
from profileapi import ProfileAPI
from generate_profile.main import LinearModel
from note_global.data_handler import DataHandler


# create profile handler
#config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'profile_config.json')
config_file = r'C:\Users\KDUWADI\Desktop\NREL_Projects\BYPL-USAID\EVOLVE\src\server\profile_config.json'

if not os.path.exists(config_file):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'docker_config_profile.json')
    #config_file = r'evolve\src\server\docker_config_profile.json'

with open(config_file,'r') as file:
    config_dict = json.load(file)

profile_handler_instance = LinearModel(config_dict)

# create a data handler
#config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.json')
config_file=r'C:\Users\KDUWADI\Desktop\NREL_Projects\BYPL-USAID\EVOLVE\src\server\config.json'

if not os.path.exists(config_file):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'docker_config_main.json')
    #config_file = r'evolve//src//server//docker_config_main.json'

with open(config_file, 'r') as file:
    data_config = json.load(file)
        
data_handler_instance = DataHandler(data_config)

app = Flask(__name__)
CORS(app)


@app.route('/profile',methods=["POST"])
def get_profile():
    api_instance = ProfileAPI(request.json, profile_handler_instance)
    return api_instance.get_data()

@app.route('/getdata',methods=["POST"])
def get_data():

    api_instance = APIData(request.json, data_handler_instance )

    data = api_instance.get_data()
    print(data['date']['data'][:10])
    print(data['dt_metric'])
    print(data['dt_metric_new'])
    return api_instance.get_data()

@app.route('/register', methods=["POST"])
def register():

    response = request.json
    response['isLogged'] = False
    if 'userdata.p' not in os.listdir(os.getcwd()):
        data = {}
        with open('userdata.p','wb') as picklehandle:
            pickle.dump(data,picklehandle)
    else:
        with open('userdata.p','rb') as picklehandle:
            data = pickle.load(picklehandle)
            
    user_data = request.json
    if user_data['password'] != user_data['passwordConfirmation']:
        response['registrationErrors'] = 'Registration failed, password did not match!!'
    else:
        if user_data['email'] in data:
            response['registrationErrors'] = 'Registration failed, user already exists!!'
        else:
            response['registrationErrors'] = f'User {user_data["email"]} registered'
            data[user_data['email']] = user_data['password']
            with open('userdata.p','wb') as picklehandle:
                pickle.dump(data,picklehandle)
            response['isLogged'] = True
            response['password'] = '************'
            response['passwordConfirmation'] = '***********'
    
    return response

@app.route('/authenticate', methods=["POST"])
def authenticate():

    response = request.json
    if 'userdata.p' not in os.listdir(os.getcwd()):
        data = {}
        with open('userdata.p','wb') as picklehandle:
            pickle.dump(data,picklehandle)
    else:
        with open('userdata.p','rb') as picklehandle:
            data = pickle.load(picklehandle)
            
    user_data = request.json
    
    if user_data['email'] in data:
        if user_data['password'] == data[user_data['email']]:
            response['registrationErrors'] = 'Success'
            response['isLogged'] = True
            response['password'] = '************'
            response['passwordConfirmation'] = '***********'
        else:
            response['registrationErrors'] = 'Sign In failed, incorrect password !'

    else:
        response['registrationErrors'] = 'Sign In failed, incorrect username and/or password !'
    
    return response


if __name__ == '__main__':
    app.run(debug=True)
