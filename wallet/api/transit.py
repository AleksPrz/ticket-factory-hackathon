
#####  N  O         S  I  R  V  E

# [START setup]
# [START imports]
import json
import os
import uuid

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import BatchHttpRequest
from google.oauth2.service_account import Credentials
from google.auth import jwt, crypt
# [END imports]

class Transit:
    """Demo class for creating and managing Transit passes in Google Wallet.

    Attributes:
        key_file_path: Path to service account key file from Google Cloud
            Console. Environment variable: GOOGLE_APPLICATION_CREDENTIALS.
        base_url: Base URL for Google Wallet API requests.
    """

    def __init__(self):
        self.key_file_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS',
                                            '../primera-plus-3ae47-e355045cae6b.json')
        # Set up authenticated client
        self.auth()

    # [END setup]

    # [START auth]
    def auth(self):
        """Create authenticated HTTP client using a service account file."""
        self.credentials = Credentials.from_service_account_file(
            self.key_file_path,
            scopes=['https://www.googleapis.com/auth/wallet_object.issuer'])

        self.client = build('walletobjects', 'v1', credentials=self.credentials)

    # [END auth]

    # [START createClass]
    def create_class(self, issuer_id: str, class_suffix: str) -> str:
        """Create a class.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for this pass class.

        Returns:
            The pass class ID: f"{issuer_id}.{class_suffix}"
        """

        # Check if the class exists
        try:
            self.client.transitclass().get(resourceId=f'{issuer_id}.{class_suffix}').execute()
        except HttpError as e:
            if e.status_code != 404:
                # Something else went wrong...
                print(e.error_details)
                return f'{issuer_id}.{class_suffix}'
        else:
            print(f'Class {issuer_id}.{class_suffix} already exists!')
            return f'{issuer_id}.{class_suffix}'

        new_class = {
            'id': f'{issuer_id}.{class_suffix}',
            'issuerName': 'Grupo Flecha Amarilla',
            'reviewStatus': 'UNDER_REVIEW',
            'logo': {
                'sourceUri': {
                    'uri':
                        'https://res.cloudinary.com/dlrmqdoyf/image/upload/v1711757100/Imagen_destacada_nvm2wk.jpg'
                },
                'contentDescription': {
                    'defaultValue': {
                        'language': 'es-ES',
                        'value': 'Logo description'
                    }
                }
            },
            'transitType': 'BUS'
        }

        response = self.client.transitclass().insert(body=new_class).execute()

        print('Class insert response')
        print(response)

        return f'{issuer_id}.{class_suffix}'

    # [END createClass]

    # [START updateClass]
    def update_class(self, issuer_id: str, class_suffix: str) -> str:
        # PENDING
        pass
    
    # [END updateClass]

    # [START patchClass]
    def patch_class(self, issuer_id: str, class_suffix: str) -> str:
        pass

    # [END patchClass]

    # [START addMessageClass]
    def add_class_message(self, issuer_id: str, class_suffix: str, header: str,
                          body: str) -> str:
        """Add a message to a pass class.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for this pass class.
            header (str): The message header.
            body (str): The message body.

        Returns:
            The pass class ID: f"{issuer_id}.{class_suffix}"
        """

        # Check if the class exists
        try:
            response = self.client.transitclass().get(resourceId=f'{issuer_id}.{class_suffix}').execute()
        except HttpError as e:
            if e.status_code == 404:
                print(f'Class {issuer_id}.{class_suffix} not found!')
                return f'{issuer_id}.{class_suffix}'
            else:
                # Something else went wrong...
                print(e.error_details)
                return f'{issuer_id}.{class_suffix}'

        response = self.client.transitclass().addmessage(
            resourceId=f'{issuer_id}.{class_suffix}',
            body={'message': {
                'header': header,
                'body': body
            }}).execute()

        print('Class addMessage response')
        print(response)

        return f'{issuer_id}.{class_suffix}'

    # [END addMessageClass]

    
    
    pass
