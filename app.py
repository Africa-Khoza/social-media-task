import grequests
import os
from flask import Flask
import time
import json


app = Flask(__name__)

@app.route("/")
async def social_network_activity():
    """
    * Fetches number of social media posts with predetermined retries on failed requests.
    * Uses a grequests to send http requests in parallel as well as reading responses as they come.
    * To optimise endpoint response time, we group retries on failed requests instead of retrying
      failed requests individually.
    :return: A json of {"Socila_media_platform": number_of_posts}
    """
    urls = {
        "twitter": 'https://takehome.io/twitter',
        "facebook": 'https://takehome.io/facebook',
        "instagram": 'https://takehome.io/instagram',
    }
    start_time = time.time()
    json_response = {}
    urls_to_retry = {}
    max_retries = 4  # Adjust max number of retries here.
    retries = 0
    retry = True  # True for the first run

    while retry:
        retry = False
        app_names = list(urls.keys())
        responses = [grequests.get(u) for u in urls.values()]

        for index, resp in grequests.imap_enumerated(responses, size=3):
            if resp.status_code == 200:
                resp_content = resp.content.decode()
                resp_dict = json.loads(resp_content)
                json_response[app_names[index]] = len(resp_dict)
                print("Received response from %s" % app_names[index])
            else:
                print("Failed with %s" % app_names[index])
                if retries < max_retries:
                    retry = True
                    print("Will be retrying: %s" % app_names[index])
                    urls_to_retry[app_names[index]] = urls[app_names[index]]
                else:
                    # We've run out of retries, take the L
                    print("Maxed out retries with %s" % app_names[index])
                    json_response[app_names[index]] = "Failed"

        if retry:
            print("Retrying... %s" % urls_to_retry)
            retries += 1
            urls = urls_to_retry
            urls_to_retry = {}

    print("--- %s seconds ---" % (time.time() - start_time))

    return json_response


if __name__ == '__main__':
    os.system('python -m flask --app app --debug run')
