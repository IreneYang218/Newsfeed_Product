import pandas as pd
import numpy as np
import re
import math
from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Read in data
roles = pd.read_csv("data/roles.csv")

@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'GET':
		query = request.args.get("q")
		try:
			return ('{"data":' + roles.to_json(orient='records') + "}")
		except:
			return "Error occurred!"

if __name__ == '__main__':
  app.run( 
	host="0.0.0.0",
	port=int("5000"),
        threaded=True
  )
