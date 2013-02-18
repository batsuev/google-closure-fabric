from setuptools import setup

setup(
    name="google_closure_fabric",
    version="0.0.4",
    author="Aleksandr Batsuev",
    author_email="batsuev@gmail.com",
    description="fabric module for simplifying google closure integration",
    license="BSD",
    keywords="google closure gjslint soy",
    url="https://github.com/batsuev/google-closure-fabric",
    packages=['google_closure_fabric', 'google_closure_fabric.gjslint_ext'],
    long_description=open('README.md', 'r').read(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    requires=[
        "fabric"
    ],
    dependency_links=[
        "http://closure-linter.googlecode.com/files/closure_linter-latest.tar.gz"
    ]
)