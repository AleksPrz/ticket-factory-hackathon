import requests

LOCALHOST = "http://127.0.0.1:5003"
DATABASE_URL = "http://127.0.0.1:5003"
TICKET_FACTORY_URL = "http://127.0.0.1:5001/factory/create-ticket"

test_data = {
    "email": "migtorruco@gmail.com",
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

def main():
    response = requests.post(url = TICKET_FACTORY_URL, json = test_data)
    print(response.text)

def test_get():
    id = 1
    url = f"{LOCALHOST}/get/ticket/{id}"
    response = requests.get(url = url)
    print(response.text)

def test_post():
    url = LOCALHOST + "/post/ticket"
    response = requests.post(url = url, data = test_data)
    print(response.text)

if __name__ == '__main__':
    main()