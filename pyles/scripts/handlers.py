"""
some command classes that should be registered with the entry point "pyles_command"
"""
import colander
import os
import subprocess
import shlex

class VirtualEnvInput(colander.MappingSchema):
    destination = colander.SchemaNode(colander.String(), 
                                      description="the location of the new virtual environment", default=os.path.abspath("."))
    interpreter = colander.SchemaNode(colander.String(),
                                      description="the python interpreter to base the virtual environment on")


class CreateVirtualEnv(object):
    """
    create a virtual environment
    """
    def advertise(self):
        return dict(description=self.__doc__, params=VirtualEnvInput())

    def execute(self, **kw):
        interpreter = kw["interpreter"]
        destination = kw["destination"]
        cmd = shlex.split("virtualenv -p %s %s" % (interpreter, destination))
        return subprocess.check_call(cmd)

