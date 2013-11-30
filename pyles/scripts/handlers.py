"""
some command classes that should be registered with the entry point "pyles_command"
"""
import colander
import os
import subprocess
import shlex
from .. import template
import contextlib

@contextlib.contextmanager
def working_dir(path):
    previous = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(previous)


TEMPLATE_ROOT = os.path.join(os.path.dirname(os.path.abspath(template.__file__)), "templates")

INTERPRETER = colander.SchemaNode(colander.String(),
                                  description="the python interpreter to base the virtual environment on",
                                  default="python")

class VirtualEnvInput(colander.MappingSchema):
    destination = colander.SchemaNode(colander.String(), 
                                      description="the location of the new virtual environment", 
                                      default=os.path.abspath("."))
    interpreter = INTERPRETER


class BuildoutInput(colander.MappingSchema):
    destination = colander.SchemaNode(colander.String(),
                                      description="the location of the new bulidout")
    interpreter = INTERPRETER

class CreateVirtualEnv(object):
    """
    create a virtual environment
    assumes: virtualenv is installed in the path
    """
    def advertise(self):
        return dict(description=self.__doc__, params=VirtualEnvInput())

    def execute(self, **kw):
        interpreter = kw["interpreter"]
        destination = kw["destination"]
        cmd = shlex.split("virtualenv -p %s %s" % (interpreter, destination))
        return subprocess.check_call(cmd)



class CreateBuildoutSkeleton(object):
    """
    creates a buildout +virtualenv ready for hacking, 

    assumes virtualenv is installed in the path
    """
    TEMPLATE_PATH = os.path.join(TEMPLATE_ROOT, "buildout")

    def advertise(self):
        return dict(description=self.__doc__, params=BuildoutInput())

    def execute(self, **kw):
        interpreter = kw["interpreter"]
        destination = os.path.abspath(kw["destination"])
        os.makedirs(destination)
        v = CreateVirtualEnv()
        v_env_dest = os.path.join(destination, ".env")
        v.execute(destination=v_env_dest,
                  interpreter=interpreter)
        for f in template.enum_files(self.TEMPLATE_PATH):
            template.render(f, template.resolve_destination(f,
                                                            templ_base=self.TEMPLATE_PATH,
                                                            dest_base=destination,
                                                            context={}),
                            {})
        bootstrap = "%s %s" % (os.path.join(v_env_dest, "bin", "python"),
                               os.path.join(destination, "bootstrap.py"))
        buildout = "%s -c %s" % (os.path.join(destination, "bin", "buildout"),
                                 os.path.join(destination, "buildout.cfg"))

        with working_dir(destination):
            subprocess.check_call(shlex.split(bootstrap))
            return subprocess.check_call(shlex.split(buildout))
