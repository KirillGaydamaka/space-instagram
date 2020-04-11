from pathlib import Path
from PIL import Image
from os import listdir
from instabot import Bot
from dotenv import load_dotenv
import os

import fetch_spacex
import fetch_hubble


def resize_image(original_name, target_name, target_size):
    image = Image.open(original_name)
    image.thumbnail((target_size, target_size))
    image.save(target_name, format="JPEG")


def resize_all_images(originals_path, targets_path, target_size):
    for filename in listdir(originals_path):
        original_name = '{}/{}'.format(originals_path, filename)
        target_name = '{}/{}'.format(targets_path, filename)
        resize_image(original_name, target_name, target_size)


def main():
    Path('./images').mkdir(parents=True, exist_ok=True)

    fetch_spacex.fetch_spacex_last_launch()
    fetch_hubble.fetch_hubble_images('printshop')

    Path('./images_resized').mkdir(parents=True, exist_ok=True)

    target_size = 1080
    resize_all_images('./images', './images_resized', target_size)

    load_dotenv()
    login = os.getenv('INSTAGRAM_LOGIN')
    password = os.getenv('INSTAGRAM_PASSWORD')

    bot = Bot()
    bot.login(username=login, password=password)

    for filename in listdir('./images_resized'):
        bot.upload_photo('./images_resized/{}'.format(filename), caption=filename.split('.')[0])


if __name__ == '__main__':
    main()
