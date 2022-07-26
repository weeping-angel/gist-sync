#-- title: Example Gist
#-- description: Sample gist calling ipinfo.io
#-- tags: python, requests

# Import
import requests
from pprint import pprint

#%%
# Make the request
resp = requests.get('https://ipinfo.io')

#%%
# Print the result
pprint(resp.json())