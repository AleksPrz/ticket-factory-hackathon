from ticket_api import create_factory_api

api = create_factory_api()

if __name__ == "__main__":
    api.run(debug = True, host = "0.0.0.0", port = 5001)