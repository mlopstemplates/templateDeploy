import os
import json
import time
import subprocess
from json import JSONDecodeError


def main():
    template_file = os.environ.get("INPUT_ARMTEMPLATE_FILE", default="deploya.json")
    template_params_file = os.environ.get("INPUT_ARMTEMPLATEPARAMS_FILE", default="deploy.parama.json")
    PAT_TOKEN="SAmpleToken"
    Repo_NAME="SampleRepo"
    SubscriptionID="SampleSubscription"
    template_file_file_path = os.path.join(".cloud", ".azure", template_params_file)
    print(template_file_file_path)
    os.chmod(template_file_file_path,stat.S_IRWXU)
    template_file_json = open(template_file_file_path, "w")
    json_object = json.load(template_file_json)
    #json_object["parameters"]["subscriptionID"]["value"]=SubscriptionID
    #json_object["parameters"]["PatToken"]["value"]=PAT_TOKEN
    #json_object["parameters"]["GitRepo"]["value"]=Repo_NAME
    #json.dump(json_object, template_file_json) 
    #template_file_json.close() 
    
    template_file_jsonR = open(template_file_file_path, "r")
    json_objectR = json.load(template_file_jsonR)
    template_file_jsonR.close() 
    print(json_objectR)

if __name__ == "__main__":
    main()
