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

    if not os.path.exists(zip_path):
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

def __append_to_gitignore(project_path, closure_dir):
    with open("%s/.gitignore" % quote(project_path), "a") as ignore_file:
        ignore_file.write(closure_dir)

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

def install_closure_templates(path):
    print('Installing google templates from %s' % CLOSURE_TEMPLATES)
    __download_and_unzip(CLOSURE_TEMPLATES, path, 'google-closure-templates')

def bootstrap(project_path, dir_name = 'google-closure'):
    """
    Setup google closure templates, stylesheets and library into project.
    """
    path = os.path.join(project_path, dir_name)
    if not os.path.exists(path):
        os.mkdir(path)

    update_closure_library(path)
    install_closure_stylesheets(path)
    install_closure_templates(path)

    if os.path.exists(os.path.join(project_path, '.git')):
        __append_to_gitignore(project_path, dir_name)
