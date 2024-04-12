import requests

localhost = "http://127.0.0.1:5001"

test_data = {
    "object_suffix" : "hackatonprueba461",
    "email": "alexis4g2@gmail.com",
    "passenger_name" : "Valeria Lee Almeyda",
    "seat_number" : "13",
    "origin" : "Campeche",
    "destination" : "Guadalajara",
    "date" : "03-04-2024",
    "day" : "MIERCOLES",
    "hour" : "4:40",
    "time" : "TARDE",
    "boarding_gate" : "59",
    "category" : "ADULTO",
    "billing_token" : "123456789",
    "total_payment" : 100.00,
    "payment_method" : "Tarjeta de debito",
    "operation_number" : 58,
    "service_number" : 77
}

response = requests.post(url = f"{localhost}/factory/create-ticket", json = test_data)

print(response.text)