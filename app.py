import flask
import yaml

'''
The follow variables must be specified in secret:
CLIENT_ACCESS_TOKEN: Client access token from DialogFlow
PAGE_ACCESS_TOKEN: Facebook page access token
VERIFY_TOKEN: Verification token for Facebook chatbot
'''
secretFile = open("secret.yaml")
secretDict = yaml.load(secretFile,  Loader=yaml.FullLoader)
secretFile.close()






