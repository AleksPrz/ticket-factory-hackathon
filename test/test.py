import requests

localhost = "http://127.0.0.1"

issuer = "3388000000022334672"
class_suffix = "hackathonclase"
object_suffix = "hackatonobjeto1"


ticket = {
        "category" : "Completo",
        "passenger_name" : "Miguel",
        "origin" : "Tabasco",
        "destination" : "Guadalajara",
        "date " : "21-03-2024",
        "hour" : "12:30 TARDE",
        "seat_number" : "17",
        "status" : "ACTIVO",
        "boarding_gate" : "83",
        "qr_value" : "LOREMIPSUMDJDJDJD",    
        }
data = {"issuer_id": issuer, "class_suffix": class_suffix, "object_suffix": object_suffix, "ticket":ticket}

class_data = {"issuer_id": issuer, "class_suffix": class_suffix}

#response = requests.post(f"{localhost}:5003/create-class", json = class_data)
response = requests.post(f"{localhost}:5003/create-pass", json = data)

print(response.text)
print(response.json())