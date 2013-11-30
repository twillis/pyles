import colander as _c
import argparse
from .. import utils


def get_input(param, arg_ctx=None, _input=input):
    """repeat until something validates, not thrilled about the impl here
    with the while

    """
    prompt = "%s\n%s: " % (param.description, param.label)
    not_ok = True

    while not_ok:
        not_ok = False
        try:
            return param.deserialize(getattr(arg_ctx, param.name, None) or _input(prompt))
        except _c.Invalid:
            not_ok = True


def prepare_command(cmd, parser, cmd_map):
    cmd_name = utils.camel_to_snake(cmd.__class__.__name__)
    cp = parser.add_parser(cmd_name, description=cmd.description)
    result = cmd.advertise()
    for x in result["params"].children:
        cp.add_argument("--%s" % x.name, dest=x.name, help=x.description)

    cmd_map[cmd_name] = cmd


def main():
    #enum commands via entry points
    parser = argparse.ArgumentParser(prog="pyles",
                                     usage="use this to help do things in your project", 
                                     description="like generate things like controllers, models, and views")
    sp = parser.add_subparsers(dest="command")
    cmd_map = {}
    c = CommandExample()
    prepare_command(c, sp, cmd_map)

    params = {}
    args = parser.parse_args()
    cmd = cmd_map[args.command]
    print(cmd.description)

    for x in cmd.advertise()["params"].children:
        params[x.name] = get_input(x, arg_ctx=args)

    cmd.execute(**params)


class CommandExample(object):
    """describes the interface for commands discovered via entry points @
    pyles.command

    """

    description = """this is a little command that doesn't do anything
    """

    class Args(_c.MappingSchema):
        project_dir = _c.SchemaNode(_c.String(),
                                    description="the directory where files will be generated",
                                    label="Project Directory")
        controller_name = _c.SchemaNode(_c.String(),
                                        description="The name of the new controller",
                                        label="Controller Name")

    def __init__(self):
        self.args = self.Args()

    def advertise(self):
        """return something that advertises functionality + needed params
        {description, params:colander.MappingSchema}
        """
        return dict(description=self.description, params=self.args)

    def execute(self, **kw):
        """do whatever the command is implemented to do with the args passed
        kw = context + results of colander.schema from advertise phase
        """
        print(kw)
