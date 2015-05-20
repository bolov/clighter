import os
import vim

def execfile_with_safe_import(filename, locals_for_file={}):
    import __builtin__
    from types import ModuleType

    class NonExistantModule(ModuleType):
        def __getattr__(self, key):
            return None
        __all__ = [] # support wildcard imports

    def tryimport(name, globals={}, locals={}, fromlist=[], level=-1):
        try:
            return realimport(name, globals, locals, fromlist, level)
        except ImportError:
            return NonExistantModule(name)

    realimport, __builtin__.__import__ = __builtin__.__import__, tryimport

    try:
        execfile(filename, locals_for_file)
    finally:
        __builtin__.__import__ = realimport

# returns the path to the ycm file
# from cwd up
# or the global fallback file
def get_ycm_file():
    ycm_basename = ".ycm_extra_conf.py"
    cur_dir = os.path.abspath(os.getcwd())

    while cur_dir:
        ycm_file = os.path.join(cur_dir, ycm_basename)
        if os.path.isfile(ycm_file):
            return ycm_file

        up_dir = os.path.dirname(cur_dir)
        if cur_dir == up_dir:
            break
        cur_dir = up_dir

    ycm_global_file = vim.eval("g:ycm_global_ycm_extra_conf")
    ycm_global_file = os.path.expanduser(ycm_global_file)

    if os.path.isfile(ycm_global_file):
        return ycm_global_file

    return None

def get():
    ycm_file = get_ycm_file()

    if ycm_file is None:
        return vim.eval("string(g:clighter_compile_args)")

    l = {}
    ycm_args = execfile_with_safe_import(ycm_file, l)

    ycm_args = l['flags']

    return str(ycm_args)

