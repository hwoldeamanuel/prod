from storages.backends.azure_storage import AzureStorage
import os
import environ

env = environ.Env()

environ.Env.read_env()



class AzureMediaStorage(AzureStorage):
    account_name =  env('AZURE_ACCOUNT_NAME')
    account_key = env('AZURE_ACCOUNT_KEY')
   
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name =  env('AZURE_ACCOUNT_NAME')
    account_key = env('AZURE_ACCOUNT_KEY')
   
    azure_container = 'static'
    expiration_secs = None