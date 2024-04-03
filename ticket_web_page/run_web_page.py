from web import create_app

web = create_app()

if __name__ == "__main__":
    web.run(debug = True, host = "0.0.0.0", port = 5002)
