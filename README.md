# Gemini Scratchpad

## Setup

```bash
# make sure you set up your python environment
# ie. virtualEnv, pipenv, or bare metal

# install pip dependencies
pip install -r requirements.txt

# create python file to hold your keys from gemini
touch keys.py

echo 'gemini_api_key = "<YOUR GEMINI API KEY>"' >> keys.py
echo 'gemini_api_secret = "<YOUR GEMINI API KEY SECRET>"' >> keys.py
```