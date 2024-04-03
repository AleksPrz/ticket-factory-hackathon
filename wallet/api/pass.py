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
                    "id": "ISSUER_ID.CLASS_ID",
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
        #PENDING
        pass
    # [END patchClass]

    # [START createObject]
    def create_object(self, issuer_id: str, class_suffix: str,
                      object_suffix: str) -> str:
        """Create an object.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for the pass class.
            object_suffix (str): Developer-defined unique ID for the pass object.

        Returns:
            The pass object ID: f"{issuer_id}.{object_suffix}"
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
                        "id": "ISSUER_ID.OBJECT_ID",
                        "classId": "ISSUER_ID.GENERIC_CLASS_ID",
                        "logo": {
                            "sourceUri": {
                            "uri": "https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg"
                            },
                            "contentDescription": {
                            "defaultValue": {
                                "language": "en-US",
                                "value": "LOGO_IMAGE_DESCRIPTION"
                            }
                            }
                        },
                        "cardTitle": {
                            "defaultValue": {
                            "language": "en-US",
                            "value": "Grupo Flecha Amarilla"
                            }
                        },
                        "subheader": {
                            "defaultValue": {
                            "language": "en-US",
                            "value": "Adulto"
                            }
                        },
                        "header": {
                            "defaultValue": {
                            "language": "en-US",
                            "value": "Alex McJacobs"
                            }
                        },
                        "textModulesData": [
                            {
                            "id": "origen",
                            "header": "Origen",
                            "body": "Campeche"
                            },
                            {
                            "id": "destino",
                            "header": "Destino",
                            "body": "Guadalajara"
                            },
                            {
                            "id": "fecha",
                            "header": "Fecha",
                            "body": "25-04-2024"
                            },
                            {
                            "id": "hora",
                            "header": "Hora",
                            "body": "12:57 MAÑANA"
                            },
                            {
                            "id": "asiento",
                            "header": "Asiento",
                            "body": "12"
                            },
                            {
                            "id": "activo",
                            "header": "",
                            "body": "ACTIVO"
                            },
                            {
                            "id": "carril",
                            "header": "Carril",
                            "body": "59"
                            }
                        ],
                        "barcode": {
                            "type": "QR_CODE",
                            "value": "BARCODE_VALUE",
                            "alternateText": ""
                        },
                        "hexBackgroundColor": "#ffd952",
                        "heroImage": {
                            "sourceUri": {
                            "uri": "https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/google-io-hero-demo-only.png"
                            },
                            "contentDescription": {
                            "defaultValue": {
                                "language": "en-US",
                                "value": "HERO_IMAGE_DESCRIPTION"
                            }
                            }
                        }
                        }

        # Create the object
        response = self.client.genericobject().insert(body=new_object).execute()

        print('Object insert response')
        print(response)

        return f'{issuer_id}.{object_suffix}'

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
        #PENDING
    pass

    # [END patchObject]

    
