import requests

localhost = "http://127.0.0.1:5001"

test_data = {
    "object_suffix" : "hackatonprueba211",
    "email": "alexis4g2@gmail.com",
    "passenger_name" : "Miguel",
    "seat_number" : "12",
    "origin" : "Campeche",
    "destination" : "Guadalajara",
    "date" : "25-03-2024",
    "day" : "LUNES",
    "hour" : "4:40",
    "time" : "TARDE",
    "boarding_gate" : "59",
    "category" : "ADULTO",
    "billing_token" : "123456789",
    "total_payment" : 100.00,
    "payment_method" : "Tarjeta de debito",
    "operation_number" : 56,
    "service_number" : 76
}

response = requests.post(url = f"{localhost}/factory/create-ticket", json = test_data)

print(response.text)