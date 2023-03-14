from flask import Flask, request
from models.plate_reader import PlateReader
import logging
from PIL import UnidentifiedImageError
import io
import requests
from plate_client import PlateClient, MyException


app = Flask(__name__)
plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')
plate_client = PlateClient()


def read_data(data):
    im = io.BytesIO(data)
    try:
        result = plate_reader.read_text(im)
    except UnidentifiedImageError:
        return {'error': 'invalid image'}, 400
    return {'name': result}


@app.route('/')
def hello():
    return '<h1><center>Hello user!</center></h1>'


# <url>:8080/readNumber : body <image bytes>
# {"name": "o123e11"}
@app.route('/readNumber', methods=["POST"])
def read_number():
    body = request.get_data()
    return read_data(body)


# <url>:8080/readNumberById?id=10022
# <url>:8080 : body: {"id": "10022"}
# -> {"name": "o123e11"}
@app.route('/readNumberById')
def read_remote_image():
    if 'id' not in request.args:
        return {'error': 'invalid args'}, 400
    image_id = request.args.get('id')
    try:
        result = plate_client.read_number_by_id(image_id)
    except MyException as err:
        return err.message, err.status_code
    return result


# <url>:8080/readArray?id=10022&id=9965
# -> {"10022": "с181мв190", "9965": "о101но750"}
@app.route('/readArray')
def read_array():
    if 'id' not in request.args:
        return {'error': 'invalid args'}, 400
    arr = request.args.getlist('id')
    try:
        result = plate_client.read_array(arr)
    except MyException as err:
        return err.message, err.status_code
    return {image_id:res for image_id, res in zip(arr, result)}


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
