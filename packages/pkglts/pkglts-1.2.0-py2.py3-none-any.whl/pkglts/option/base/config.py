from os.path import abspath, basename


parameters = [
    ("pkgname", basename(abspath("."))),
    ("namespace", None),
    ("url", None),
    ("authors", [("moi", "moi@email.com")])
]


def is_valid_identifier(name):
    """ Check that name is a valid python identifier
    sort of back port of "".isidentifier()
    """
    try:
        compile("%s=1" % name, "test", 'single')
        return True
    except SyntaxError:
        return False


def check(env):
    """Check the validity of parameters in working environment.

    Args:
        env (jinja2.Environment):  current working environment

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    pkgname = env.globals['base'].pkgname
    namespace = env.globals['base'].namespace

    if "." in pkgname:
        invalids.append('pkgname')
    elif not is_valid_identifier(pkgname):
        invalids.append('pkgname')

    if namespace is not None:
        if "." in namespace:
            invalids.append('namespace')
        elif not is_valid_identifier(namespace):
            invalids.append('namespace')

    return invalids


def after(pkg_cfg):
    del pkg_cfg  # unused
    print("base: after main config")
