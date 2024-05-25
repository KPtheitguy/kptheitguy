import boto3
import json

class AWSAuthenticator:
    def __init__(self, credentials_file='inputs.json'):
        self.credentials_file = credentials_file
        self.secrets = self._get_credentials_from_file()

    def _get_credentials_from_file(self):
        with open(self.credentials_file, 'r') as file:
            secrets = json.load(file)
        return secrets

    def get_session(self):
        # Create a boto3 session using the retrieved secret keys
        session = boto3.Session(
            aws_access_key_id=self.secrets['Access_key'],
            aws_secret_access_key=self.secrets['Secret_access_key'],
            region_name=self.secrets['region_name']
        )
        return session
