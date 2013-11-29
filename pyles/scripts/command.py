import argparse
import inspect
from . import handlers as handlers_mod
from functools import partial

enum_functions = partial(inspect.getmembers, predicate=callable)
handlers = dict([(k, v) for k, v in enum_functions(handlers_mod)])
parser = argparse.ArgumentParser(prog="pyles",
                                 usage="use this to help do things in your project", 
                                 description="like generate things like controllers, models, and views")

sp = parser.add_subparsers(dest="command")

for k, v in handlers.items():
    cp = sp.add_parser(k, description=v.__doc__)
    # args


def main():
    args = parser.parse_args()

    cmd = handlers.get(args.command, None)
    if cmd:
        cmd()
    else:
        print(args)
