from aiohttp import web
import json

import sys
import os
from stat import S_ISFIFO

piped_content = sys.stdin.read() if S_ISFIFO(os.fstat(0).st_mode) else ''

# first position or stdin: content
# serving content as json dump
# -f --file: serve content as file
# -d --debugger: use pdb
# -v --verbose: print all


def ensure_bytes(x):
    if not isinstance(x, bytes):
        x = bytes(str(x).encode("utf8"))
    return x


def echo(request):
    dc = getattr(request, "__dict__")
    return json.dumps({k: str(v) for k, v in dc.items()})


def route_wrapper(reply, use_pdb=False, printing=False):
    async def route_function(request):
        if use_pdb:
            import pdb
            pdb.set_trace()
        if hasattr(reply, '__call__'):
            result = ensure_bytes(reply(request))
        else:
            result = ensure_bytes(reply)
        if printing:
            print("result", result)
        return web.Response(body=result)
    return route_function


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description='Mock an API with mocka.')
    parser.add_argument('--debug', '-d', action="store_true",
                        help='Uses "pdb" to drop you into the request, before replying')
    parser.add_argument('--port', '-p', type=int, default=8080,
                        help='Port where to host')
    parser.add_argument('--verbose', '-v', action="store_true",
                        help='Talks.... a lot.')
    parser.add_argument('--file', '-f', nargs=1,
                        help='Loads file')
    args = parser.parse_args()

    args.file = args.file[0] if args.file else None
    return args


def main():
    """ This is the function that is run from commandline with `yagmail` """
    app = web.Application()

    args = parse_args()

    METHODS = ["GET", "POST", "OPTIONS", "HEAD"]
    DTYPES = ["text", "json", "echo", 'file']

    RESPONSES = {'text': "Hello, world!",
                 'json': json.dumps({"hello": "world!"}),
                 'echo': echo,
                 'file': json.dumps}

    if args.file:
        with open(args.file) as f:
            RESPONSES['file'] = json.dumps(f.read())

    if piped_content:
        try:
            RESPONSES['json'] = json.dumps(json.loads(piped_content))
        except json.decoder.JSONDecodeError:
            print("info: cannot serve '{}' as JSON".format(piped_content))
        RESPONSES['text'] = piped_content

    ROUTER = {}
    for m in METHODS:
        for d in DTYPES:
            ROUTER[(m.lower(), d)] = route_wrapper(RESPONSES[d], args.debug, args.verbose)

    for r, route_fn in ROUTER.items():
        app.router.add_route(r[0], '/{}_{}'.format(*r), route_fn)

    for m in METHODS:
        route_fn = ensure_bytes(json.dumps(sorted(['/' + '_'.join(x) for x in ROUTER])))
        app.router.add_route(m, '/', route_wrapper(route_fn))

    web.run_app(app, port=args.port)

if __name__ == "__main__":
    main()
