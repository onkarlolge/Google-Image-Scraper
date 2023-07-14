# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
#Import libraries
import os
import concurrent.futures
from GoogleImageScraper import GoogleImageScraper
from patch import webdriver_executable
import time


import os
start_time=time.time()
def worker_thread(search_key):
    brandname, keyword = search_key.split('-')  # Extract the brand name and keyword from the search key
    image_directory = os.path.normpath(os.path.join(os.getcwd(), 'photos', brandname))
    os.makedirs(image_directory, exist_ok=True)  # Create the directory if it doesn't exist

    image_scraper = GoogleImageScraper(
        webdriver_path,
        image_directory,  # Use the brandname/keyword directory as the image path
        keyword,  # Use the keyword as the search key
        number_of_images,
        headless,
        min_resolution,
        max_resolution,
        max_missed)
    image_urls = image_scraper.find_image_urls()
    image_scraper.save_images(image_urls, keep_filenames)

    # Release resources
    del image_scraper


if __name__ == "__main__":
    # Define file path
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))
    print('image path', image_path)

    # Add new search key into array ["brandname-keyword", "brandname-keyword"]
    input_string = input('Enter elements of a list separated by commas to search (example: brandname-keyword,brandname-keyword): ')
    print("\n")
    user_list = input_string.split(',')
    # print list
    print('list: ', user_list)

    # Parameters
    number_of_images = 50  # Desired number of images
    headless = True  # True = No Chrome GUI
    min_resolution = (800, 600)  # Minimum desired image resolution
    max_resolution = (9999, 9999)  # Maximum desired image resolution
    max_missed = 50  # Max number of failed images before exit
    number_of_workers = 16  # Number of "workers" used
    keep_filenames = False  # Keep original URL image filenames

    # Run each search_key in a separate thread
    # Automatically waits for all threads to finish
    # Removes duplicate strings from search_keys
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        executor.map(worker_thread, user_list)
end_time=time.time()
exec_time=end_time-start_time
print('total execution time',exec_time)
