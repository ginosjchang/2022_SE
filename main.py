from flask import Flask
from src import create_app
import os

app = create_app()

if __name__ == "__main__":

    app.run(port=7414, debug=True)