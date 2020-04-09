import requests
from pathlib import Path
from PIL import Image
from os import listdir

TARGET_SIZE = 1080


def download_image(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    api_url = 'https://api.spacexdata.com/v3/launches/latest'
    response = requests.get(api_url)
    response.raise_for_status()

    image_links = response.json()['links']['flickr_images']

    for image_number, image_link in enumerate(image_links):
        download_image(image_link, './images/spacex{}.jpg'.format(image_number))


def download_hubble_image(id):
    api_url = 'http://hubblesite.org/api/v3/image/{}'.format(id)
    response = requests.get(api_url, verify=False)
    response.raise_for_status()

    images_info = response.json()['image_files']
    last_image_url = images_info[-1]['file_url']
    last_image_nosslproblem_url = 'https://hubblesite.org/{}'.format(last_image_url[28:])
    image_filename = './images/{}.{}'.format(id, get_url_extension(last_image_url))
    download_image(last_image_nosslproblem_url, image_filename)


def fetch_hubble_images(collection):
    api_url = 'http://hubblesite.org/api/v3/images/{}'.format(collection)
    response = requests.get(api_url, verify=False)
    response.raise_for_status()

    images_info = response.json()
    for image_info in images_info:
        print(image_info['id'])
        download_hubble_image(image_info['id'])
    print(images_info)


def get_url_extension(url):
    return url.split('.')[-1]


def resize_image(original_name, target_name):
    image = Image.open(original_name)
    image.thumbnail((TARGET_SIZE, TARGET_SIZE))
    image.save(target_name, format="JPEG")

def resize_all_images(originals_path, targets_path):
    for filename in listdir(originals_path):
        original_name = '{}/{}'.format(originals_path, filename)
        target_name = '{}/{}'.format(targets_path, filename)
        resize_image(original_name, target_name)

Path('./images').mkdir(parents=True, exist_ok=True)

#fetch_spacex_last_launch()
#fetch_hubble_images('printshop')

Path('./images_resized').mkdir(parents=True, exist_ok=True)

resize_image('3892.jpg', 'rs.jpg')

resize_all_images('./images', './images_resized')