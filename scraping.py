import json

import requests
from bs4 import BeautifulSoup as Soup
from requests_toolbelt.multipart.encoder import MultipartEncoder


def main(file, requests=None):
    url = "https://www.qrrd.ru/?action=ajaxfunc&sa=load_qrimg"

    encoder = MultipartEncoder(
        fields={
            "delete_url": "https://www.qrrd.ru/?action=ajaxfunc",
            "custom_url": "/qrread/",
            "custom_dir": "/qrread/",
            "files": ("hueta.png", open(file, "rb"), "multipart/form-data")
        }
    )

    response = requests.post(

        url=url,
        data=encoder,
        headers={"Content-Type": encoder.content_type},

    )

    text = json.loads(response.text)
    files = text['files']
    for i in files:
        j = i

    try:
        qrcode_viever = j['description2'] + ' ' + j['description']

        return qrcode_viever
    except KeyError:
        print_except = 'Не удалось распознать 🙁'
        return print_except


def create(data, file):
    url = "https://www.qrrd.ru/?action=ajaxfunc&sa=createqr"

    fields = {
        'textqr': data,
        'qrsize': 4,
        'color_back': '#ffffff',
        'color_code': '#000000',

    }

    response = requests.post(url=url, data=fields)
    soup = Soup(response.content, 'html.parser')

    for link in soup.find_all('img'):
        image = link.get('src')

    with open(file, 'wb') as target:
        a = requests.get(image)
        target.write(a.content)
    return image
