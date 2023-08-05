from importlib import import_module
from inspect import isfunction
import json
from os.path import exists, splitext
from pkgutil import walk_packages

from pkglts.local import pkg_full_name

from .create_node_def import create_node_def


def find_plugin_categories(txt):
    if txt is None:
        return []

    if '__plugin__' not in txt:
        return []

    for line in txt.splitlines():
        if '__plugin__' in line:
            cat_txt = line.strip().split(":")[1].strip()
            return [c.strip() for c in cat_txt.split(",")]


def parse_plugins(pkg):
    """Parse recursively all plugins in a given package

    Notes: write plugin def files

    Args:
        pkg: (Package) a python package object

    Returns:
        None
    """
    for imp, modname, ispkg in walk_packages(pkg.__path__):
        loader = imp.find_module(modname)
        mod = import_module("%s.%s" % (pkg.__name__, loader.fullname))
        if ispkg:
            parse_plugins(mod)
        else:
            root_pth = splitext(mod.__file__)[0]
            plugins = {}
            if hasattr(mod, '__all__'):
                item_names = mod.__all__
            else:
                item_names = dir(mod)
            for item_name in item_names:
                item = getattr(mod, item_name)
                if isfunction(item):
                    for cat in find_plugin_categories(item.__doc__):
                        if cat == "node":
                            pth = "%s_%s.wkf" % (root_pth, item_name)
                            plugins[item_name] = (pth, create_node_def(item))

            if len(plugins) > 0:
                for item_name, (pth, idef) in plugins.items():
                    if exists(pth):
                        with open(pth, 'r') as f:
                            old_idef = json.load(f)

                        idef['id'] = old_idef['id']

                    with open(pth, 'w') as f:
                        json.dump(idef, f, indent=2)


def main(env, target=".", overwrite=False):
    """Main function called to walk the package

    Args:
        env: (dict of (str, dict)) package configuration parameters
        target (str): place to write plugin def into
        overwrite (bool): whether or not to overwrite previous definition
                          files. Default to False.
    """
    del target
    del overwrite
    pkg = import_module(pkg_full_name(env))
    parse_plugins(pkg)
