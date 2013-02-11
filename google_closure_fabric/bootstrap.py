__author__ = 'alex'

import os, urllib, zipfile
from fabric.api import local
from pipes import quote
from shutil import rmtree

"""
Module for installing closure library, templates and stylesheets into project.
TODO: windows support
"""

CLOSURE_LIBRARY_SVN = 'http://closure-library.googlecode.com/svn/trunk/'
CLOSURE_STYLESHEETS = 'http://closure-stylesheets.googlecode.com/files/closure-stylesheets-20111230.jar'
CLOSURE_TEMPLATES = 'http://closure-templates.googlecode.com/files/closure-templates-for-javascript-latest.zip'
PLOVR = 'http://plovr.googlecode.com/files/plovr-eba786b34df9.jar'

def __svn_up(path):
    try:
        local('svn up %s' % path)
    except StandardError:
        raise StandardError('svn not found. Please install console svn')

def __svn_checkout(url, path):
    try:
        local('svn checkout %s %s' % (url, quote(path)))
    except StandardError:
        raise StandardError('svn not found. Please install console svn')

def __download_and_unzip(url, path, dir_name):
    zip_path = os.path.join(path, dir_name + '.zip')

    if os.path.exists(zip_path):
        os.unlink(zip_path)

    urllib.urlretrieve(
        url,
        zip_path
    )

    target_path = os.path.join(path, dir_name)
    if os.path.exists(target_path):
        rmtree(target_path)

    zip = zipfile.ZipFile(zip_path)
    zip.extractall(path=target_path)
    zip.close()

    os.remove(zip_path)

def __append_to_gitignore(ignore_string, project_path):
    gitignore = os.path.join(project_path, '.gitignore')
    ignore_string += '\n'
    if os.path.exists(gitignore):
        content = open(gitignore, 'r').read()
        if not ignore_string in content:
            open(gitignore, "a").write(ignore_string)
    else:
        open(gitignore, "w").write(ignore_string)

def update_closure_library(path):
    lib_path = os.path.join(path, 'google-closure-library')
    if os.path.exists(lib_path) and os.path.exists(os.path.join(lib_path,'.svn')):
        __svn_up(lib_path)
    else:
        __svn_checkout(CLOSURE_LIBRARY_SVN, lib_path)

def install_closure_stylesheets(path):
    print('Installing google closure stylesheets from %s' % CLOSURE_STYLESHEETS)
    stylesheets_path = os.path.join(path, 'google-closure-stylesheets')
    if os.path.exists(stylesheets_path):
        rmtree(stylesheets_path)
    os.mkdir(stylesheets_path)
    urllib.urlretrieve(
        CLOSURE_STYLESHEETS,
        os.path.join(stylesheets_path, 'closure-stylesheets.jar')
    )

def install_plovr(path):
    print('Installing plovr from %s' % PLOVR)
    plovr_path = os.path.join(path, 'plovr')
    if os.path.exists(plovr_path):
        rmtree(plovr_path)
    os.mkdir(plovr_path)
    urllib.urlretrieve(
        PLOVR,
        os.path.join(plovr_path, 'plovr.jar')
    )

def install_closure_templates(path):
    print('Installing google closure templates from %s' % CLOSURE_TEMPLATES)
    __download_and_unzip(CLOSURE_TEMPLATES, path, 'google-closure-templates')

def bootstrap(project_path, dir_name=None, templates=True, stylesheets=True, library=True, plovr=True):
    """
    Setup google closure templates, stylesheets and library into project.
    """

    paths_file = '.closure_paths'
    if dir_name is None:
        if os.path.exists(paths_file):
            dir_name = open(paths_file, 'r').read()
        else:
            dir_name = 'google_closure'

    path = os.path.join(project_path, dir_name)
    if not os.path.exists(path):
        os.mkdir(path)

    if library:
        update_closure_library(path)
    if stylesheets:
        install_closure_stylesheets(path)
    if templates:
        install_closure_templates(path)
    if plovr:
        install_plovr(path)

    with open(paths_file, 'w') as paths:
        paths.write(dir_name)

    if os.path.exists(os.path.join(project_path, '.git')):
        __append_to_gitignore(ignore_string=dir_name + '/', project_path=project_path)
        __append_to_gitignore(ignore_string=paths_file, project_path=project_path)
