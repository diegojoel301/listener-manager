import logging
from flask import Flask, Response

app = Flask(__name__)

# Configuración de logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    return 'Hola Mundo!'

@app.route('/logs')
def logs():
    with open('app.log', 'r') as log_file:
        content = log_file.read()
        return Response(content, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

