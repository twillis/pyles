"""this is the main command driver for pyles and here's what it does.

#1: builds a map of all entry points registered with "pyles_command"


#2: gets input from user for chosen command


#3: executes chosen command with user input


a pyles_command entry point has the following expectations.



#1: callable with no args produces an instance with an advertise
#method and an execute method


#2: advertise returns a dict with keys "description" and "params",
#"description" is a string presumed to be a help message for the
#command, "params" is a colander Mapping schema that describes the
#arguments needed from the user to proceed



#3: execute is called with arguments from user in **kw style

"""
import colander
import argparse
from .. import utils
import pkg_resources

def get_input(param, arg_ctx=None, _input=input):
    """repeat until something validates, not thrilled about the impl here
    with the while

    """
    label = getattr(param, "title", getattr(param, "name", "param"))
    if param.default:
        label = "%s[%s]" % (label, param.default)

    prompt = "%s\n%s: " % (param.description, label)
    not_ok = True

    while not_ok:
        not_ok = False
        try:
            return param.deserialize(getattr(arg_ctx, param.name, None) or _input(prompt) or param.default)
        except colander.Invalid as ex:
            for msg in ex.messages():
                print(msg)
            not_ok = True


def prepare_command(cmd, parser, cmd_map):
    """
    add cmd to cmd_map and add it's arguments to the parser'
    """
    cmd_name = utils.camel_to_snake(cmd.__class__.__name__)
    result = cmd.advertise()
    cp = parser.add_parser(cmd_name, description=result.get("description", None))

    for x in result["params"].children:
        cp.add_argument("--%s" % x.name, dest=x.name, help=x.description)

    cmd_map[cmd_name] = cmd


def iter_entry_points(group):
    for ep in pkg_resources.iter_entry_points(group):
        yield ep.load()

def main():
    #enum commands via entry points
    parser = argparse.ArgumentParser(prog="pyles",
                                     usage="use this to help do things in your project", 
                                     description="like generate things like controllers, models, and views")
    sp = parser.add_subparsers(dest="command")
    cmd_map = {}

    for C in iter_entry_points("pyles_command"):
        c = C()
        prepare_command(c, sp, cmd_map)

    params = {}
    args = parser.parse_args()
    cmd = cmd_map.get(args.command, None)

    if not cmd:
        parser.print_help()
        return

    result = cmd.advertise()
    print(result.get("description", None))

    for x in result.get("params", colander.MappingSchema()).children:
        params[x.name] = get_input(x, arg_ctx=args)

    cmd.execute(**params)
