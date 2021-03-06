import requests
import download_image
import os


def download_hubble_image(image_id):
    api_url = 'http://hubblesite.org/api/v3/image/{}'.format(image_id)
    response = requests.get(api_url, verify=False)
    response.raise_for_status()

    images_info = response.json()['image_files']
    last_image_url = images_info[-1]['file_url']
    last_image_nosslproblem_url = 'https://hubblesite.org/{}'.format(last_image_url[28:])
    image_filename = './images/{}{}'.format(image_id, os.path.splitext(last_image_url)[1])
    download_image.download_image(last_image_nosslproblem_url, image_filename)


def fetch_hubble_images(collection):
    api_url = 'http://hubblesite.org/api/v3/images/{}'.format(collection)
    response = requests.get(api_url, verify=False)
    response.raise_for_status()

    images_info = response.json()
    for image_info in images_info:
        download_hubble_image(image_info['id'])
