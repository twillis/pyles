"""
there are a couple modes for this....


some commands will render a file with context as src/dest/ctx

some commands will render several files with directories rendered from context like so

ctx: {project_dir: my_proj, controller: profile}
src/{{project_dir}}/test/test_{{controller}}.py => dest/my_proj/test/test_profile.py

"""


import unittest
import os
from pyles import template

__here__ = os.path.abspath(os.path.dirname(__file__))


class TestPathResolution(unittest.TestCase):
    def testPathSrcDestNoTemplate(self):
        src = os.path.abspath("src/test_model.py")
        dest = os.path.abspath("dest/test_model.py")
        self.assertEquals(template.resolve_destination(src,
                                                       templ_base="./src",
                                                       dest_base="./dest"),
                          dest)

    def testPathSrcDestWithTemplate(self):
        src = os.path.abspath("src/{{test_dir}}/test_model.py")
        dest = os.path.abspath("dest/test/test_model.py")
        self.assertEquals(template.resolve_destination(src,
                                                       templ_base="./src",
                                                       dest_base="./dest",
                                                       context={"test_dir":
                                                                "test"}),
                          dest)


class TestEnumDir(unittest.TestCase):
    def testEnumDir(self):
        ctx = {"project_dir": "./mybanginproject",
               "test_dir": "{{project_dir}}/test",
               "controller_name": "Profile"}
        for f in template.enum_files(os.path.join(__here__, "data/create_controller"), predicate=template.NOT_CONTEXT):
            dest = template.resolve_destination(f, 
                                                templ_base=os.path.join(__here__, "data/create_controller"), 
                                                dest_base=os.path.join(__here__), 
                                                context=ctx)
            template.assert_path_contained_in(__here__, dest)
            print(dest)
