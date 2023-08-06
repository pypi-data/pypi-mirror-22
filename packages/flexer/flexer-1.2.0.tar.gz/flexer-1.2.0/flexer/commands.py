import click
import getpass
import glob
import json
import os
import pip
import zipfile

from flexer.config import (
    CONFIG_FILE,
    DEFAULT_CMP_URL,
)
from flexer.context import FlexerContext
from flexer.runner import Flexer
from flexer.utils import write_yaml_file

BUILD_EXCLUDE_DIRS = [
    ".git",
    ".cache",
    "__pycache__",
]


def config():
    url_prompt = 'CMP URL (default is "%s"): ' % DEFAULT_CMP_URL
    user_prompt = 'CMP API Key: '
    pass_prompt = 'CMP API Secret: '

    url = ""
    key = "KEY"
    secret = "SECRET"
    if os.sys.stdin.isatty():
        url = raw_input(url_prompt)
        key = raw_input(user_prompt)
        secret = getpass.getpass(pass_prompt)

    config = {
        'verify_ssl': True,
        'regions': {
            'default': {
                'cmp_url': url or DEFAULT_CMP_URL,
                'cmp_api_key': key,
                'cmp_api_secret': secret,
            }
        }
    }
    write_yaml_file(CONFIG_FILE, config)

def run(handler, event, config, cmp_client):
    event = json.loads(event)
    handler = "main.%s" % handler
    context = FlexerContext(cmp_client=cmp_client)
    if config is not None:
        context.config = json.loads(config)

    result = Flexer().run(event=event,
                          context=context,
                          handler=handler,
                          debug=True)
    return json.loads(result)


def install_deps(source):
    click.echo("Installing dependencies...", err=True)
    lib_dir = os.path.join(source, "lib")
    for f in glob.glob(os.path.join(source, "requirements*.txt")):
        click.echo('Found "%s". Installing...' % f, err=True)
        pip.main(["install", "-t", lib_dir, "-U", "-r", f])


def build_zip(source, target, exclude=None):
    if exclude is None:
        exclude = []

    exclude += BUILD_EXCLUDE_DIRS
    click.echo("Archiving everything under %s as %s" % (source, target),
               err=True)
    with zipfile.ZipFile(target, "w") as zf:
        for dirname, subdirs, files in os.walk(source, topdown=True):
            subdirs[:] = [d for d in subdirs if d not in exclude]
            prefix = strip_dir_path(source, dirname)
            if prefix:
                zf.write(dirname, prefix)

            for filename in files:
                if filename.endswith(".pyc"):
                    continue

                actual_file_path = os.path.join(dirname, filename)
                if actual_file_path == target:
                    continue

                zipped_file_path = os.path.join(prefix, filename)
                zf.write(actual_file_path, zipped_file_path)


def strip_dir_path(source, dirname):
    """Keep the folder structure after the path folder by
    a) appending a '/' at the end of directory names
    b) removing the first character from a directory name if it is a '/'
    The result should look like this:
    file1.txt
    folder1/
    folder1/folder2/
    folder1/folder2/file2.txt
    """
    prefix = ""
    prefix = dirname.replace(source, "")
    if prefix != "":
        prefix += "/"
        if prefix.startswith("/"):
            prefix = prefix[1:]

    return prefix


def test(verbose=False):
    import unittest
    from flexer.connector_tests.test_base import BaseConnectorTest
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    runner.run(unittest.makeSuite(BaseConnectorTest))
