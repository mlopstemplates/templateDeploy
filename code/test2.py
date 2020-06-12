import os
import json
import time
import subprocess
from json import JSONDecodeError
from utils import AMLConfigurationException, ActionDeploymentError, AMLExperimentConfigurationException, required_parameters_provided, mask_parameter, convert_to_markdown, load_pipeline_yaml, load_runconfig_yaml, load_runconfig_python


def main():
    template_file = os.environ.get("INPUT_ARMTEMPLATE_FILE", default="deploya.json")
    template_params_file = os.environ.get("INPUT_ARMTEMPLATEPARAMS_FILE", default="deploy.parama.json")
    PAT_TOKEN="SAmpleToken"
    Repo_NAME="SampleRepo"
    SubscriptionID="SampleSubscription"
    template_file_json = open(template_file, "w")
    json_object = json.load(template_file_json)
    json_object["parameters"]["subscriptionID"]["value"]=SubscriptionID
    json_object["parameters"]["PatToken"]["value"]=PAT_TOKEN
    json_object["parameters"]["GitRepo"]["value"]=Repo_NAME
    json.dump(json_object, template_file_json) 
    template_file_json.close() 
    
    template_file_jsonR = open(template_file, "r")
    json_objectR = json.load(template_file_jsonR)
    template_file_json.close() 
    print(json_objectR)

if __name__ == "__main__":
    main()
