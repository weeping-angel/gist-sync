# Repo Gist Sync

![https://pypi.python.org/pypi/repo-gist-sync](https://img.shields.io/pypi/v/repo-gist-sync?label=PyPI)
![https://pypistats.org/packages/repo-gist-sync](https://img.shields.io/pypi/dm/repo-gist-sync?color=darkgreen&label=Downloads)


A library to synchronize git repository to Github Gists

```mermaid
    graph TD;

    A(local machine)
    A -->|push| B(Github repository)
    B -->|Github Actions| C(Gists)
    B -->|Github Actions| E(Gists)
    B -->|Github Actions| F(Gists)
    C --> D(Embeds)
    E --> G(Embeds)
    F --> H(Embeds)
    C --> I(Embeds)
    E --> J(Embeds)
    F --> K(Embeds)
```

## Installation

Install from [PyPI](https://pypi.org/project/repo-gist-sync).

```shell
pip install repo-gist-sync
```

Dependencies: `requests`, `click`

## Example

1. Write the Code as follows:

- `get_user_id.py`

```python
#-- title: Get User's ID
#-- description: Code to retrieve user_id from username
#-- tags: python, medium_api, medium_api_py


# Import libraries
import os
from medium_api import Medium

#%%
# Get RAPIDAPI_KEY from the environment
api_key = os.getenv('RAPIDAPI_KEY')

#%%
# Create a `Medium` Object
medium = Medium(api_key)

#%%
# Get the `User` Object using "username" and print ID
user = medium.user(username="nishu-jain")
print(user.user_id)
```

- `get_user_id_output.txt`

```plain
1985b61817c3
```

2. Sync using `gistdirsync` CLI tool.

```shell
gistdirsync --auth-token $GIST_TOKEN --directory /path/to/folder
```

3. Resulting Gist looks like this:

<script src="https://gist.github.com/weeping-angel/c4e694ee6f2ede9d7261acd87152e8f7"></script>

## Continuous Deployment with Github Actions


```yaml
name: GIST CD on main branch and example directory change

on:
  push:
    paths:
      - examples/**

jobs:
  build:
    if: github.ref == 'refs/heads/main'

    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ['3.8']

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install repo-gist-sync
      run: pip install repo-gist-sync

    - name: Use "gistsyncdir" on "examples" directory
      run: gistdirsync --auth-token ${{ secrets.GIST_TOKEN }} --directory ./examples/
```

## Features

- Supports python (`.py`) and shellscripts (`.sh`)
- Can write metadata in file itself
- Break the code in smaller snippets
- can save the output in the corresponding gist by naming the file as "_filename_**_output.txt**"


