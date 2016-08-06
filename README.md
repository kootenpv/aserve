## aserve (pre-alpha)

The goal of aserve is to make it easy to "asynchronously serve an API". If you want to
serve some text, json, or echo a request: aserve enables quick
testing... just run `aserve`.

- Hackathon: give your buddy an endpoint with a statically served JSON
- Server-to-server: viewing how a request looks like with headers etc
- Send your custom response: use `pdb` to drop in a request and return a response manually
- New: Serve a python file with functions!

### Features

- Easy to use, just a command line required ;)
- Asynchronous
- Serve different types of data
- Automatically supports GET/POST/HEAD/OPTIONS
- Pipe data to aserve to serve it: `cat some.json | aserve`
- **UPDATE**: Serve all functions [automagically](#serving-python-functions) with `aserve my_filename.py`

### Installation

Only works on Python 3.5+ at the moment.

    pip3.5 install aserve

### How to:

```
usage: aserve [-h] [--debug] [--port PORT] [--verbose] [--file FILE] [--sleep SLEEP]

Asynchronously Serve an API with aserve.

optional arguments:
  -h, --help                   show this help message and exit
  --debug, -d                  Uses "pdb" to drop you into the request, BEFORE replying
  --port PORT, -p PORT         Port where to host
  --verbose, -v                Talks.... a lot.
  --file FILE, -f FILE         Loads file (COMING VERY SOON)
  --sleep SLEEP, -s SLEEP      seconds to wait before delivering
```

### Default routes

```
/get_echo
/get_file
/get_json
/get_text
/head_echo
/head_file
/head_json
/head_text
/options_echo
/options_file
/options_json
/options_text
/post_echo
/post_file
/post_json
/post_text
```

### Serving python functions

Given `filenamy.py`:

```python
def concatenate(x, y):
    return x + y

import asyncio
async def concatenate_async(x, y):
    await asyncio.sleep(1)
    return x + y
```

this file can be served with aserve using `aserve /path/to/filename.py`.

You can then GET (with query parameters):

```python
import requests
url = "http://localhost:port/filename/concatenate"
requests.get(url + "?x=hello&y=world").text
requests.get(url + "_async" + "?x=hello&y=world").text
```

and POST:

```python
import requests
import json
url = "http://localhost:port/filename/concatenate"
requests.get(url, data=json.dumps({"x": "hello", "y": "word"})).json
requests.get(url + "_async", data=json.dumps({"x": "hello", "y": "word"})).json
```


### Caveats

Currently, it uses `aiohttp` and asyncio, and aserve is only available from Python 3.5+. It should be possible in the future to use a different backend.
Reasons for a different backend might be to not require any other installation, or perhaps to support older versions of Python.
