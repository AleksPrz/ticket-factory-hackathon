import requests

localhost = "http://127.0.0.1"

issuer = "3388000000022334672"
class_suffix = "hackathonclase"
object_suffix = "hackatonobjeto1"
start_time = "2024-04-04T01:20:50.52Z"
end_time = "2024-04-05T05:20:50.52Z"

data = {"issuer_id" : issuer, "object_suffix": object_suffix, "header": "Hola", "body": "mun2"}

response = requests.post(f"{localhost}:5000/send-message", json = data)

print(response)