from google.cloud import storage

# Replace 'path/to/your/keyfile.json' with the path to your downloaded JSON key file
key_path = '/Users/yangyujie/Documents/GCP/developer-yyj-737cd34829e1.json'

# Create a Storage client using the service account key
storage_client = storage.Client.from_service_account_json(key_path)
print(storage_client)
# Now you can use storage_client to interact with Google Cloud Storage
