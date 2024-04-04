import requests

LOCALHOST = "http://127.0.0.1:5003"

datos = {
    "email": "example2@you",
    "passenger_name" : "PRUEBA FINAL",
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
    test_get()

def test_get():
    for i in range(1, 5):
        url = f"{LOCALHOST}/get/ticket/{i}"
        response = requests.get(url = url)
        print(response.text)

def test_post():
    url = LOCALHOST + "/post/ticket"
    response = requests.post(url = url, data = datos)
    print(response.text)

if __name__ == '__main__':
    main()