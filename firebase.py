import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate(
    'rihal-be-challenge-firebase-adminsdk-164xq-60c6cb5319.json'
)
firebase_app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'rihal-be-challenge.appspot.com'
})

firebase_bucket = storage.bucket()
