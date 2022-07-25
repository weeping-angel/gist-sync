"""
Sample Gist in the examples of "repo-gist-sync" project
"""

# Import
import requests
from pprint import pprint

#%%
# Make the request
resp = requests.get('https://ipinfo.io')


#%%
# Print the result
pprint(resp.json())