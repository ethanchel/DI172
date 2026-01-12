# Instructions :
# Using the requests and time modules, create a function which returns the amount of time it takes a webpage to load (how long it takes for a complete response to a request).
# Test your code with multiple sites such as google, ynet, imdb, etc.

import requests
import time
def time_webpage_load(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()

    if response.status_code == 200:
        load_time = end_time - start_time
        return load_time
    else:
        raise Exception(f"Failed to load webpage. Status code: {response.status_code}")
# Example usage:
urls = ["https://solvertouch.com"]
for url in urls:
    try:
        load_time = time_webpage_load(url)
        print(f"Time taken to load {url}: {load_time:.4f} seconds")
    except Exception as e:
        print(e)
