import os
import json
import time
import subprocess
from azureml.core import Workspace, Experiment
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.pipeline.core import PipelineRun
from azureml.exceptions import AuthenticationException, ProjectSystemException, AzureMLException, UserErrorException
from adal.adal_error import AdalError
from msrest.exceptions import AuthenticationError
from json import JSONDecodeError
from utils import AMLConfigurationException, ActionDeploymentError, AMLExperimentConfigurationException, required_parameters_provided, mask_parameter, convert_to_markdown, load_pipeline_yaml, load_runconfig_yaml, load_runconfig_python


def deploy_functionApp(template_path, parameters_file_path,resource_group):
    try:
        command = ('az group deployment create -g {resource_group} --template-file "{template_path}" --parameters "{parameters_file_path}" -o json').format(
            template_path=template_path, parameters_file_path=parameters_file_path, resource_group=resource_group)
        print(command)
        app_create = subprocess.check_output(command, shell=True)
        app_create_json = json.loads(app_create)
        return app_create_json # may here return just the values required to be returned
    except Exception as ex:
        raise ActionDeploymentError(ex)
        
def update_templateParameters(template_params_file):
    pat_token=os.environ.get("INPUT_PAT_TOKEN", default="")
    repo_name=os.environ.get("INPUT_GITHUB_REPO", default="")
    subscriptionID=os.environ.get("INPUT_SUBSCRIPTION_ID", default="")
    template_file_file_path = os.path.join(".cloud", ".azure", template_params_file)
    template_file_jsonR = open(template_file_file_path, "r")
    json_object = json.load(template_file_jsonR)
    template_file_jsonR.close()
    
    json_object["parameters"]["subscriptionID"]={}
    json_object["parameters"]["subscriptionID"]["value"]=subscriptionID
    
    json_object["parameters"]["GitHubRepo"]={}
    json_object["parameters"]["GitHubRepo"]["value"]=repo_name
    
    json_object["parameters"]["PatToken"]={}
    json_object["parameters"]["PatToken"]["value"]=pat_token
    
    template_file_json = open(template_file_file_path, "w")
    json.dump(json_object, template_file_json) 
    template_file_json.close() 
    template_file_jsonR2 = open(template_file_file_path, "r")
    json_object2 = json.load(template_file_jsonR2)
    print("printing updated parameters file")
    print(json_object2)
    template_file_jsonR2.close()
 
    
def main():
    # # Loading input values
    # print("::debug::Loading input values")
    template_file = os.environ.get("INPUT_ARMTEMPLATE_FILE", default="deploya.json")
    template_params_file = os.environ.get("INPUT_ARMTEMPLATEPARAMS_FILE", default="deploy.parama.json")
    azure_credentials = os.environ.get("INPUT_AZURE_CREDENTIALS", default="{}")
    resource_group = os.environ.get("INPUT_RESOURCE_GROUP", default="newresource_group")
 
    update_templateParameters(template_params_file)
    try:
        azure_credentials = json.loads(azure_credentials)
    except JSONDecodeError:
        print("::error::Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS")
        raise AMLConfigurationException(f"Incorrect or poorly formed output from azure credentials saved in AZURE_CREDENTIALS secret. See setup in https://github.com/Azure/aml-workspace/blob/master/README.md")

    # Checking provided parameters
    print("::debug::Checking provided parameters")
    required_parameters_provided(
        parameters=azure_credentials,
        keys=["tenantId", "clientId", "clientSecret"],
        message="Required parameter(s) not found in your azure credentials saved in AZURE_CREDENTIALS secret for logging in to the workspace. Please provide a value for the following key(s): "
    )
    #secret_unmasked=azure_credentials.get("clientSecret", "").replace("`","\\`")
    print("printed  secret")
    # Mask values
    print("::debug::Masking parameters")
    mask_parameter(parameter=azure_credentials.get("tenantId", ""))
    mask_parameter(parameter=azure_credentials.get("clientId", ""))
    #mask_parameter(parameter=azure_credentials.get("clientSecret", ""))
    mask_parameter(parameter=azure_credentials.get("subscriptionId", ""))
    
    # Loading parameters file
    #print("::debug::Loading parameters file")
    template_file_file_path = os.path.join(".cloud", ".azure", template_file)
    template_params_file_path = os.path.join(".cloud", ".azure", template_params_file)
    
    tenant_id=azure_credentials.get("tenantId", "")
    service_principal_id=azure_credentials.get("clientId", "")
    service_principal_password=azure_credentials.get("clientSecret", "").replace("`","\\`")
    print(service_principal_password)
    print("here")
    command = ('az login --service-principal --username {APP_ID} --password \"{PASSWORD}\" --tenant {TENANT_ID}').format(
          APP_ID=service_principal_id, PASSWORD=service_principal_password, TENANT_ID=tenant_id)
    print(command)
    try:
       app_create = subprocess.check_output(command, shell=True)
       print(app_create)
    except Exception as ex:
       print(ex)
    
    #print(deploy_machineLearningWorkspace(ml_template_file_file_path ,ml_template_params_file_path , resource_group))
    print(deploy_functionApp(template_file_file_path,template_params_file_path , resource_group))


if __name__ == "__main__":
    main()
