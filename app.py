# Import necessary modules and classes

from server import app

# Entry point of the application
if __name__ == "__main__":
    app.run(debug=True, port=5555)
