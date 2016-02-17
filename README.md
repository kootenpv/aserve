## mocka (pre-alpha)

The goal of mocka is to make it easy to "mock an API". If you want to
serve some text, json, or echo a request: mocka enables quick
testing.

- Hackathon: give your buddy an endpoint with a statically served JSON
- Server-to-server: viewing how a request looks like
- Send your custom response: use `pdb` to drop in a request and return a response manually

### Features

- Easy to use, just a command line required ;)
- Asynchronous
- Serve different types of data
- Automatically supports GET/POST/HEAD/OPTIONS
- Pipe data to mocka to serve it: `cat some.json | mocka`

### Installation

Only works on Python 3.5+ at the moment.

    pip3.5 install mocka

### How to:

```
usage: mocka [-h] [--debug] [--port PORT] [--verbose] [--file FILE] [--sleep SLEEP]

Mock an API with mocka.

optional arguments:
  -h, --help                   show this help message and exit
  --debug, -d                  Uses "pdb" to drop you into the request, BEFORE replying
  --port PORT, -p PORT         Port where to host
  --verbose, -v                Talks.... a lot.
  --file FILE, -f FILE         Loads file (COMING VERY SOON)
  --sleep SLEEP, -s SLEEP      seconds to wait before delivering
```

### Looking for direction

I will most likely completely rewrite this library at some point, just trying to get some ideas for now.
Perhaps helping with speedtests or something. Perhaps to enable easy of setting up an API.

### Caveats

Currently, it uses `aiohttp` and asyncio, and mocka is only available from Python 3.5+. It should be possible in the future to use a different backend.
Reasons for a different backend might be to not require any other installation, or perhaps to support
