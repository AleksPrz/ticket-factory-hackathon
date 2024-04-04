import requests

localhost = "http://127.0.0.1"

issuer = "3388000000022334672"
class_suffix = "hackathonclase"
object_suffix = "hackatonobjeto1"

data = {"issuer_id" : issuer, "class_suffix": class_suffix, "object_suffix": object_suffix, "header": "Hola", "body": "mundo"}

response = requests.post(f"{localhost}:5000/send-message", json = data)

print(response)