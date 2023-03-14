import requests

class PlateClient:
    def __init__(self, url: str):
        self.url = url

    def read_number(self, im) -> str:
        res = requests.post(
            f'{self.url}/readNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=im,
            timeout=1
        )
        return res.json()['name']
    
    def upper(self):
        pass


if __name__ == '__main__':
    client = PlateClient('http://127.0.0.1:8080')
    with open('images/10022.jpg', 'rb') as im:
        res = client.read_number(im)
    print(res)