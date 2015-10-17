#!/usr/bin/env python

import pyonep
from flask import Flask

app = Flask(__name__)
_1P = pyonep.onep.OnepV1()

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
