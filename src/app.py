from flask import Flask, request
from models.plate_reader import PlateReader
import logging
from PIL import UnidentifiedImageError
import io

app = Flask(__name__)
plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')


@app.route('/')
def hello():
    return '<h1><center>Hello w!</center></h1>'


@app.route('/toUpper')
def to_upper():
    if 's' not in request.args:
        return 'invalid args', 400
    s = request.args.get('s', 'missing')
    return {
        'result': s.upper()
    }

# <url>:8080/readNumber : body <image bytes>
# {"name": "o123e11"}
@app.route('/readNumber', methods=["POST"])
def read_number():
    body = request.get_data()
    im = io.BytesIO(body)
    try:
        result = plate_reader.read_text(im)
    except UnidentifiedImageError:
        return {'error': 'invalid image'}, 400
    return {
        'name': result
    }

if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
