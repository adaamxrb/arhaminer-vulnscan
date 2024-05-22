from flask import Flask, request, jsonify
import subprocess
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/scan', methods=['POST'])
def scan_domain():
    data = request.get_json()
    domain = data.get('domain')
    
    if not domain:
        logging.error("Domain is required but not provided.")
        return jsonify({'error': 'Domain is required'}), 400

    try:
        #Nmap
        logging.info(f"Running Nmap scan on {domain}")
        nmap_output = subprocess.check_output(['nmap', domain], stderr=subprocess.STDOUT)
        nmap_result = nmap_output.decode('utf-8')

         # Run Nikto and capture the output
        logging.info(f"Running Nikto scan on {domain}")
        nikto_output = subprocess.check_output(['nikto', '-h', domain], stderr=subprocess.STDOUT)
        nikto_result = nikto_output.decode('utf-8')
        
        # Combine results
        result = f"Nmap Result:\n{nmap_result}\n\nNikto Result:\n{nikto_result}"
    except subprocess.CalledProcessError as e:
        logging.error(f"Scan failed: {e.output.decode('utf-8')}")
        result = e.output.decode('utf-8')
    except Exception as e:
        logging.exception("An unexpected error occurred")
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
