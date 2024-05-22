from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_domain():
    domain = request.form['domain']
    data = {"domain": domain}
    
    try:
        response = requests.post('http://localhost:5002/scan', json=data)
        response.raise_for_status()
        result = response.json().get('result')
    except requests.exceptions.RequestException as e:
        result = f"Request failed: {e}"
    except Exception as e:
        result = f"An unexpected error occurred: {e}"
    
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
