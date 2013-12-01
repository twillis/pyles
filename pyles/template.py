import os
from jinja2 import Template
from .utils import camel_to_snake as _c
import sys
from shutil import copyfile
PY3 = sys.version_info[0] == 3

NOOP = lambda x: True
CONTEXT = lambda x: x == "template.json"
NOT_CONTEXT = lambda x: not CONTEXT(x)


# http://eli.thegreenplace.net/2011/10/19/perls-guess-if-file-is-text-or-binary-implemented-in-python/
int2byte = (lambda x: bytes((x,))) if PY3 else chr

_text_characters = (
    b''.join(int2byte(i) for i in range(32, 127)) +
    b'\n\r\t\f\b')

def is_text_file(filepath, blocksize=512):
    """ Uses heuristics to guess whether the given file is text or binary,
        by reading a single block of bytes from the file.
        If more than 30% of the chars in the block are non-text, or there
        are NUL ('\x00') bytes in the block, assume this is a binary file.
    """
    with open(filepath, "rb") as fileobj:
        block = fileobj.read(blocksize)
        if b'\x00' in block:
            # Files with null bytes are binary
            return False
        elif not block:
            # An empty file is considered a valid text file
            return True

        # Use translate's 'deletechars' argument to efficiently remove all
        # occurrences of _text_characters from the block
        nontext = block.translate(None, _text_characters)
        return float(len(nontext)) / len(block) <= 0.30


def assert_path_contained_in(base, path):
    base = os.path.abspath(base)
    path = os.path.abspath(path)
    assert not os.path.relpath(path, base).startswith(".."), "%s not contained in %s" % (path, base)


def compute_destination_for_source(src, templ_base=".", dest_base=".", context=None):
    """
    given params return destination file path for src file path
    handle templated paths based on context
    """
    context = context or {}
    context = {k: Template(v).render(context) for k, v in context.items()}
    templ_base = os.path.abspath(templ_base)
    dest_base = os.path.abspath(dest_base)
    src = os.path.abspath(os.path.join(templ_base, src))
    src_rel = os.path.relpath(src, start=templ_base)

    assert_path_contained_in(templ_base, src)
    assert templ_base != dest_base, "%s and %s are the same" % (templ_base, dest_base)

    return os.path.abspath(Template(os.path.join(dest_base,
                        src_rel)).render({k: _c(v) for k, v in context.items()}))


def iter_files(base_dir, predicate=None):
    """
    yield files with abspath where predicate or all
    """
    predicate = predicate or NOOP
    for d, _, files in os.walk(base_dir):
        for f in [x for x in files if predicate(x)]:
            yield os.path.abspath(os.path.join(d, f))


def render(src, dest, context):
    """given src path and dest path either copy the file if it is binary
    or handle as a template otherwise

    raise error if dest already exists

    """
    src = os.path.abspath(src)
    dest = os.path.abspath(dest)
    assert not os.path.exists(dest), "%s exists." % dest
    context = {k: Template(v).render(context) for k, v in context.items()}
    dest_dir = os.path.dirname(dest)
    if not (os.path.exists(dest_dir) and os.path.isdir(dest_dir)):
        os.makedirs(dest_dir)
    if not is_text_file(src):
        copyfile(src, dest)
    else:
        with open(src) as src_f:
            with open(dest, "w") as dest_f:
                dest_f.write(Template(src_f.read()).render(context))


def render_template_dir(src_dir, dest_dir, context=None):
    """ given src dir render templates to dest_dir applying context to the
    path as well as the body of the files along the way

    """
    context = context or {}
    for f in iter_files(src_dir):
        render(f, compute_destination_for_source(f,
                                      templ_base=src_dir,
                                      dest_base=dest_dir,
                                      context=context), context)
