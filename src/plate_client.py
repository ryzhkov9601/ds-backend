import requests


class MyException(Exception):
    def __init__(self, message, status_code):
        self.message = {'error': message}
        self.status_code = status_code

    def __str__(self):
        return self.message


class PlateClient:
    def __init__(self, url = 'http://127.0.0.1:8080', image_storage_url='http://51.250.83.169:7878/images'):
        self.url = url
        self.image_storage_url = image_storage_url
        self.valid_ids = ['10022', '9965']

    def read_number(self, im):
        res = requests.post(
            f'{self.url}/readNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=im,
            timeout=1
        )
        return res.json()
    
    def read_number_by_id(self, image_id):
        if image_id not in self.valid_ids:
            raise MyException('invalid id of image', 400)
        try:
            response = requests.get(
                f'{self.image_storage_url}/{image_id}',
                timeout=1
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise MyException('image not found', 400)
        except requests.exceptions.ConnectionError:
            raise MyException('can not connect', 500)
        except requests.exceptions.Timeout:
            raise MyException('request timeout', 500)
        except requests.exceptions.RequestException as err:
            raise MyException(str(err), 500)
        return self.read_number(response.content)

    def read_array(self, arr: list):
        return [self.read_number_by_id(image_id)['name'] for image_id in arr]


if __name__ == '__main__':
    client = PlateClient('http://127.0.0.1:8080')
    with open('images/10022.jpg', 'rb') as im:
        res = client.read_number(im)
    print(res)

    res = client.read_number_by_id('10022')
    print(res)

    res = client.read_array(['10022', '9965'])
    print(res)
