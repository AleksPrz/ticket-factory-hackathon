from api import create_api

wallet_api = create_api()

if __name__ == "__main__":
    wallet_api.run(debug = True, host = "0.0.0.0", port = 5004)