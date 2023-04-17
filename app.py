import numpy as np
from flask import Flask, request, jsonify, render_template
import subprocess
import pickle
import re
import os
import signal

app = Flask(__name__)
@app.route("/")
def home():
    return render_template('index.html')
    

@app.route('/run_script')
def run_script():
    subprocess.Popen(["streamlit", "run", "streamlit_app.py"])
    return "success"

if __name__ == "__main__":
    app.run(debug=True)