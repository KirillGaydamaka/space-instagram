import requests
import download_image


def fetch_spacex_last_launch():
    api_url = 'https://api.spacexdata.com/v3/launches/latest'
    response = requests.get(api_url)
    response.raise_for_status()

    image_links = response.json()['links']['flickr_images']

    for image_number, image_link in enumerate(image_links):
        download_image.download_image(image_link, './images/spacex{}.jpg'.format(image_number))
