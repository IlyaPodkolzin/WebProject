import os
from flask import Flask, render_template
import forms


app = Flask(__name__)
app.config['SECRET_KEY'] = 'check_check_key'


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)