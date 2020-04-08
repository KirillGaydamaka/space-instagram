import requests
from pathlib import Path


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


def get_url_extension(url):
    return url.split('.')[-1]

Path('./images').mkdir(parents=True, exist_ok=True)

fetch_spacex_last_launch()


#print(image_links)

#print(get_url_extension('//imgsrc.hubblesite.org/hvi/uploads/image_file/image_attachment/4/small_web.tif'))

download_hubble_image(1)

api_url = 'http://hubblesite.org/api/v3/images/news'
response = requests.get(api_url, verify=False)
response.raise_for_status()

images_info = response.json()
print(images_info)