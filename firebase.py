import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('firebase_config.json')
firebase_app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'gs://rihal-be-challenge.appspot.com/'
})

firebase_bucket = storage.bucket()
