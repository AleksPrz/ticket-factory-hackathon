from db import create_database

database = create_database()

if __name__ == "__main__":
    database.run(debug = True, host = "0.0.0.0", port = 5001)