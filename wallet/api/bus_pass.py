# [START setup]
# [START imports]
import json
import os
import uuid

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
from google.auth import jwt, crypt
# [END imports]

class Pass:
    """Demo class for creating and managing Generic passes in Google Wallet.

    Attributes:
        key_file_path: Path to service account key file from Google Cloud
            Console. Environment variable: GOOGLE_APPLICATION_CREDENTIALS.
        base_url: Base URL for Google Wallet API requests.
    """

    def __init__(self):
        self.key_file_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS',
                                            '../t1ck3tf4ct0ry-97c34b0abfa3.json')
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
            self.client.genericclass().get(resourceId=f'{issuer_id}.{class_suffix}').execute()
        except HttpError as e:
            if e.status_code != 404:
                # Something else went wrong...
                print(e.error_details)
                return f'{issuer_id}.{class_suffix}'
        else:
            print(f'Class {issuer_id}.{class_suffix} already exists!')
            return f'{issuer_id}.{class_suffix}'

        new_class = {
                    "id": f'{issuer_id}.{class_suffix}',
                    "classTemplateInfo": {
                        "cardTemplateOverride": {
                        "cardRowTemplateInfos": [
                            {
                            "twoItems": {
                                "startItem": {
                                "firstValue": {
                                    "fields": [
                                    {
                                        "fieldPath": "object.textModulesData['origen']"
                                    }
                                    ]
                                }
                                },
                                "endItem": {
                                "firstValue": {
                                    "fields": [
                                    {
                                        "fieldPath": "object.textModulesData['destino']"
                                    }
                                    ]
                                }
                                }
                            }
                            },
                            {
                            "twoItems": {
                                "startItem": {
                                "firstValue": {
                                    "fields": [
                                    {
                                        "fieldPath": "object.textModulesData['fecha']"
                                    }
                                    ]
                                }
                                },
                                "endItem": {
                                "firstValue": {
                                    "fields": [
                                    {
                                        "fieldPath": "object.textModulesData['hora']"
                                    }
                                    ]
                                }
                                }
                            }
                            },
                            {
                            "threeItems": {
                                "startItem": {
                                "firstValue": {
                                    "fields": [
                                    {
                                        "fieldPath": "object.textModulesData['asiento']"
                                    }
                                    ]
                                }
                                },
                                "middleItem": {
                                "firstValue": {
                                    "fields": [
                                    {
                                        "fieldPath": "object.textModulesData['activo']"
                                    }
                                    ]
                                }
                                },
                                "endItem": {
                                "firstValue": {
                                    "fields": [
                                    {
                                        "fieldPath": "object.textModulesData['carril']"
                                    }
                                    ]
                                }
                                }
                            }
                            }
                        ]
                        }
                    }
                    }

        response = self.client.genericclass().insert(body=new_class).execute()

        print('Class insert response')
        print(response)

        return f'{issuer_id}.{class_suffix}'

    # [END createClass]

    # [START patchClass]
    def patch_class(self, issuer_id: str, class_suffix: str) -> str:
        """Patch a class.

        The PATCH method supports patch semantics.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for this pass class.

        Returns:
            The pass class ID: f"{issuer_id}.{class_suffix}"
        """

        # Check if the class exists
        try:
            response = self.client.genericclass().get(resourceId=f'{issuer_id}.{class_suffix}').execute()
        except HttpError as e:
            if e.status_code == 404:
                print(f'Class {issuer_id}.{class_suffix} not found!')
                return f'{issuer_id}.{class_suffix}'
            else:
                # Something else went wrong...
                print(e.error_details)
                return f'{issuer_id}.{class_suffix}'
        # There is no 'else' statement - that means that the class HAS to exist in order to patch it!!

        # Class exists
        existing_class = response

        # [EXAMPLE] Patch the class by adding a link
        patch_body = {}
        new_link = {
            'uri': 'https://developers.google.com/wallet',
            'description': 'Homepage description'
        }

        # Check if the class has already been patched before
        if existing_class.get('linksModuleData'):
            patch_body['linksModuleData'] = existing_class.get(
                'linksModuleData')
        # Patch the class for the first time
        else:
            patch_body['linksModuleData'] = {'uris': []}

        # Add the new link to the class
        patch_body['linksModuleData']['uris'].append(new_link)

        # Note: reviewStatus must be 'UNDER_REVIEW' or 'DRAFT' for patches
        patch_body['reviewStatus'] = 'UNDER_REVIEW'

        response = self.client.genericclass().patch(
            resourceId=f'{issuer_id}.{class_suffix}',
            body=patch_body).execute()

        print('Class patch response')
        print(response)

        return f'{issuer_id}.{class_suffix}'

    # [END patchClass]

    # [START createObject]
    def create_object(self, issuer_id: str, class_suffix: str,
                      object_suffix: str, ticket: dict) -> str:
        """Create an object.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for the pass class.
            object_suffix (str): Developer-defined unique ID for the pass object.

        Returns:
            The "Add to Google Wallet" link
        """

        # Check if the object exists
        try:
            self.client.genericobject().get(resourceId=f'{issuer_id}.{object_suffix}').execute()
        except HttpError as e:
            if e.status_code != 404:
                # Something else went wrong...
                print(e.error_details)
                return f'{issuer_id}.{object_suffix}'
        else:
            print(f'Object {issuer_id}.{object_suffix} already exists!')
            return f'{issuer_id}.{object_suffix}'

        new_object = {
                        "id": f"{issuer_id}.{object_suffix}",
                        "classId": f"{issuer_id}.{class_suffix}",
                        "enableNotification": True,
                        "logo": {
                            "sourceUri": {
                            "uri": "https://res.cloudinary.com/dlrmqdoyf/image/upload/v1711679336/Marca_600_150_1_kgrfq0.png"
                            },
                            "contentDescription": {
                            "defaultValue": {
                                "language": "es-ES",
                                "value": "LOGO_IMAGE_DESCRIPTION"
                            }
                            }
                        },
                        "cardTitle": {
                            "defaultValue": {
                            "language": "es-ES",
                            "value": "Grupo Flecha Amarilla"
                            }
                        },
                        "subheader": {
                            "defaultValue": {
                            "language": "es-ES",
                            "value": f"{ticket.get("category")}"
                            }
                        },
                        "header": {
                            "defaultValue": {
                            "language": "es-ES",
                            "value": f"{ticket.get("passenger_name")}"
                            }
                        },
                        "textModulesData": [
                            {
                            "id": "origen",
                            "header": "Origen",
                            "body": f"{ticket.get("origin")}"
                            },
                            {
                            "id": "destino",
                            "header": "Destino",
                            "body": f"{ticket.get("destination")}"
                            },
                            {
                            "id": "fecha",
                            "header": "Fecha",
                            "body": f"{ticket.get("date")}"
                            },
                            {
                            "id": "hora",
                            "header": "Hora",
                            "body": f"{ticket.get("hour")}"
                            },
                            {
                            "id": "asiento",
                            "header": "Asiento",
                            "body": f"{ticket.get("seat_number")}"
                            },
                            {
                            "id": "activo",
                            "header": "",
                            "body": f"ACTIVO"
                            },
                            {
                            "id": "carril",
                            "header": "Carril",
                            "body": f"{ticket.get("boarding_gate")}"
                            }
                        ],
                        "barcode": {
                            "type": "QR_CODE",
                            "value": f"{ticket.get("qr_value")}",
                            "alternateText": ""
                        },
                        "hexBackgroundColor": "#ffd952",
                        "heroImage": {
                            "sourceUri": {
                            "uri": "https://res.cloudinary.com/dlrmqdoyf/image/upload/v1711757100/Imagen_destacada_nvm2wk.jpg"
                            },
                            "contentDescription": {
                            "defaultValue": {
                                "language": "es-ES",
                                "value": "HERO_IMAGE_DESCRIPTION"
                            }
                            }
                        }
                        }

        # Create the object
        response = self.client.genericobject().insert(body=new_object).execute()

        print('Object insert response')
        print(response)

        # Create the JWT claims
        claims = {
            'iss': self.credentials.service_account_email,
            'aud': 'google',
            'origins': ['www.example.com'],
            'typ': 'savetowallet',
            'payload': {
                # The listed classes and objects will be created
                'genericObjects': [new_object]
            }
        }

        # The service account credentials are used to sign the JWT
        signer = crypt.RSASigner.from_service_account_file(self.key_file_path)
        token = jwt.encode(signer, claims).decode('utf-8')

        print('Add to Google Wallet link')
        print(f'https://pay.google.com/gp/v/save/{token}')

        return f'https://pay.google.com/gp/v/save/{token}'

    # [END createObject]

    # [START patchObject]
    def patch_object(self, issuer_id: str, object_suffix: str) -> str:
        """Patch an object.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            object_suffix (str): Developer-defined unique ID for the pass object.

        Returns:
            The pass object ID: f"{issuer_id}.{object_suffix}"
        """

        # Check if the object exists
        try:
            response = self.client.genericobject().get(resourceId=f'{issuer_id}.{object_suffix}').execute()
        except HttpError as e:
            if e.status_code == 404:
                print(f'Object {issuer_id}.{object_suffix} not found!')
                return f'{issuer_id}.{object_suffix}'
            else:
                # Something else went wrong...
                print(e.error_details)
                return f'{issuer_id}.{object_suffix}'
        # There is no 'else' statement - that means that the class HAS to exist in order to patch it!!

        # Object exists
        existing_object = response

        # Patch the object by adding a link
        patch_body = {}
        new_link = {
            'uri': 'https://developers.google.com/wallet',
            'description': 'New link description'
        }

        # Check if the class has already been patched before
        if existing_object.get('linksModuleData'):
            patch_body['linksModuleData'] = existing_object['linksModuleData']
        # Patch the class for the first time
        else:
            patch_body['linksModuleData'] = {'uris': []}

        # Add the new link to the class
        patch_body['linksModuleData']['uris'].append(new_link)
    
        response = self.client.genericobject().patch(
            resourceId=f'{issuer_id}.{object_suffix}',
            body=patch_body).execute()

        print('Object patch response')
        print(response)

        return f'{issuer_id}.{object_suffix}'

    # [END patchObject]

    # [START batch]
    def batch_create_objects(self, issuer_id: str, class_suffix: str):
        """Batch create Google Wallet objects from an existing class.

        The request body will be a multiline string. See below for information.

        https://cloud.google.com/compute/docs/api/how-tos/batch#example

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for this pass class.
        """
        batch = self.client.new_batch_http_request()

        # Example: Generate three new pass objects
        for _ in range(3):
            # Generate a random object suffix
            object_suffix = str(uuid.uuid4()).replace('[^\\w.-]', '_')

            # See link below for more information on required properties
            # https://developers.google.com/wallet/generic/rest/v1/genericobject
            batch_object = {
                'id': f'{issuer_id}.{object_suffix}',
                'classId': f'{issuer_id}.{class_suffix}',
                'state': 'ACTIVE',
                'heroImage': {
                    'sourceUri': {
                        'uri':
                            'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg'
                    },
                    'contentDescription': {
                        'defaultValue': {
                            'language': 'en-US',
                            'value': 'Hero image description'
                        }
                    }
                },
                'textModulesData': [{
                    'header': 'Text module header',
                    'body': 'Text module body',
                    'id': 'TEXT_MODULE_ID'
                }],
                'linksModuleData': {
                    'uris': [{
                        'uri': 'http://maps.google.com/',
                        'description': 'Link module URI description',
                        'id': 'LINK_MODULE_URI_ID'
                    }, {
                        'uri': 'tel:6505555555',
                        'description': 'Link module tel description',
                        'id': 'LINK_MODULE_TEL_ID'
                    }]
                },
                'imageModulesData': [{
                    'mainImage': {
                        'sourceUri': {
                            'uri':
                                'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg'
                        },
                        'contentDescription': {
                            'defaultValue': {
                                'language': 'en-US',
                                'value': 'Image module description'
                            }
                        }
                    },
                    'id': 'IMAGE_MODULE_ID'
                }],
                'barcode': {
                    'type': 'QR_CODE',
                    'value': 'QR code'
                },
                'cardTitle': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Generic card title'
                    }
                },
                'header': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Generic header'
                    }
                },
                'hexBackgroundColor': '#4285f4',
                'logo': {
                    'sourceUri': {
                        'uri':
                            'https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg'
                    },
                    'contentDescription': {
                        'defaultValue': {
                            'language': 'en-US',
                            'value': 'Generic card logo'
                        }
                    }
                }
            }

            batch.add(self.client.genericobject().insert(body=batch_object))

        # Invoke the batch API calls
        response = batch.execute()

        print('Batch complete')

    # [END batch]
    
    # [START addMessageObject]
    def add_object_message(self, issuer_id: str, object_suffix: str, header: str, body: str) -> str:
        """Add a message to a pass object.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            object_suffix (str): Developer-defined unique ID for this pass object.
            header (str): The message header.
            body (str): The message body.

        Returns:
            The pass class ID: f"{issuer_id}.{class_suffix}"
        """
        
        self.credentials = Credentials.from_service_account_file(
            self.key_file_path,
            scopes=['https://www.googleapis.com/auth/wallet_object.issuer'])

        self.client = build('walletobjects', 'v1', credentials=self.credentials)

        # Check if the object exists
        try:
            response = self.client.genericobject().get(resourceId=f'{issuer_id}.{object_suffix}').execute()
        except HttpError as e:
            if e.status_code == 404:
                print(f'Object {issuer_id}.{object_suffix} not found!')
                return f'{issuer_id}.{object_suffix}'
            else:
                # Something else went wrong...
                print(e.error_details)
                return f'{issuer_id}.{object_suffix}'

        response = self.client.genericobject().addmessage(
            resourceId=f'{issuer_id}.{object_suffix}',
            body={'message': {
                'header': header,
                'body': body
            }}).execute()

        print('Object addMessage response')
        print(response)

        return f'{issuer_id}.{object_suffix}'

    # [END addMessageObject]