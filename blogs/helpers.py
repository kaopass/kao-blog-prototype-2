from django.conf import settings
import requests


def delete_domain(domain):
    url = f"https://api.heroku.com/apps/bear-blog/domains/{domain}"

    payload = {
        "hostname": domain
    }

    headers = {
        'content-type': "application/json",
        'accept': "application/vnd.heroku+json; version=3",
        'authorization': f'Bearer {settings.HEROKU_BEARER_TOKEN}',
    }

    response = requests.request(
        "DELETE", url, data=json.dumps(payload), headers=headers)

    print(response.text)


def add_new_domain(domain):
    url = "https://api.heroku.com/apps/bear-blog/domains"

    payload = {
        "hostname": domain
    }

    headers = {
        'content-type': "application/json",
        'accept': "application/vnd.heroku+json; version=3",
        'authorization': f'Bearer {settings.HEROKU_BEARER_TOKEN}',
    }

    response = requests.request(
        "POST", url, data=json.dumps(payload), headers=headers)

    print(response.text)

    return id
