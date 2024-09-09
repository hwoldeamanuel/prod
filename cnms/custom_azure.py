from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'paqcnmsblob' # <storage_account_name>
    account_key = 'DRMNWaWCZPYBKM7UAdCKLpTBqQGEhpb9PmFC2Huciu15tcGEyBdiHfmfozH/hyfyv2AlcOYPdwyo+AStVQrz8g==' # <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

