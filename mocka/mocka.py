import asyncio
import imp
from inspect import getmembers, isfunction
import json
import os
import sys
from stat import S_ISFIFO

from aiohttp import web


def ensure_bytes(x):
    """ Ensure 'x' is going to be served as bytes. """
    if not isinstance(x, bytes):
        x = bytes(str(x).encode("utf8"))
    return x


def echo(request):
    """ The response will reflect what the request looks like. """
    dc = getattr(request, "__dict__")
    return json.dumps({k: str(v) for k, v in dc.items()})


def route_wrapper(reply, use_pdb=False, printing=False, sleepfor=0):
    """ Wrapper to easily create routes. """
    async def route_function(request):
        status_code = 200
        reason = None
        if sleepfor:
            await asyncio.sleep(sleepfor)
        if use_pdb:
            import pdb
            pdb.set_trace()
        if hasattr(reply, '__call__'):
            result, status_code, reason = await reply(request)
            result = ensure_bytes(result)
        else:
            result = ensure_bytes(reply)
        if printing:
            print("result", result)
        return web.Response(body=result, status=status_code, reason=reason)
    return route_function


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description='Mock an API with mocka.')
    parser.add_argument("python_file", nargs="?")
    parser.add_argument('--debug', '-d', action="store_true",
                        help='Uses "pdb" to drop you into the request, BEFORE replying')
    parser.add_argument('--port', '-p', type=int, default=21487,
                        help='Port where to host')
    parser.add_argument('--verbose', '-v', action="store_true",
                        help='Talks.... a lot.')
    parser.add_argument('--file', '-f', nargs=1,
                        help='Loads file (COMING VERY SOON)')
    parser.add_argument('--sleep', '-s', type=int, default=0,
                        help='seconds to wait before delivering')
    args = parser.parse_args()

    args.file = args.file[0] if args.file else None
    if args.verbose:
        print("Going to talk a lot.")
        print("Debugging mode {}.".format(args.debug))
        if args.sleep:
            print("Sleeping between requests: {}s.".format(args.sleep))
        if args.file is not None:
            raise NotImplementedError("Planned to come soon. Check back later.")
            print("serving file at /file")
    return args


def fn_to_route(fn):

    async def routed_function(request):
        response = None
        args = None
        # return fn(request)
        if request.method == "POST":
            try:
                post_data = await request.json()
            except json.decoder.JSONDecodeError:
                post_data = await request.post()

            args = post_data
        else:
            # just to make it asyncable, but i dont know what i should have here
            _ = await request.text()
            args = request.GET
        # response
        status_code = 200
        reason = None
        try:
            response = fn(**args)
        except Exception as e:
            response, status_code, reason = "error", 500, e
        return response, status_code, reason

    return routed_function


def main():
    """ This is the function that is run from commandline with `mocka` """
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

    piped_content = sys.stdin.read() if S_ISFIFO(os.fstat(0).st_mode) else ''

    if piped_content:
        try:
            RESPONSES['json'] = json.dumps(json.loads(piped_content))
        except json.decoder.JSONDecodeError:
            print("info: cannot serve '{}' as JSON".format(piped_content))
        RESPONSES['text'] = piped_content

    ROUTER = {}
    for m in METHODS:
        for d in DTYPES:
            route = route_wrapper(RESPONSES[d], args.debug, args.verbose, args.sleep)
            ROUTER[(m.lower(), d)] = route

    if args.python_file is not None:
        args.python_file = os.path.abspath(args.python_file)
        mod_name, _ = os.path.splitext(os.path.split(args.python_file)[-1])
        py_mod = imp.load_source(mod_name, args.python_file)
        for fn_name, fn in getmembers(py_mod, isfunction):
            if fn.__module__ == py_mod.__name__:
                route_fn = route_wrapper(fn_to_route(fn), args.debug, args.verbose, args.sleep)
                app.router.add_route('POST', '/{}/{}'.format(py_mod.__name__, fn_name), route_fn)
                app.router.add_route('GET', '/{}/{}'.format(py_mod.__name__, fn_name), route_fn)

    for r, route_fn in ROUTER.items():
        app.router.add_route(r[0], '/' + '_'.join(r), route_fn)

    for m in METHODS:
        route_fn = ensure_bytes(json.dumps(sorted(['/' + '_'.join(x) for x in ROUTER])))
        app.router.add_route(m, '/', route_wrapper(route_fn, args.debug, args.verbose, args.sleep))

    web.run_app(app, port=args.port)

if __name__ == "__main__":
    main()
