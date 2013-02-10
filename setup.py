from setuptools import setup

setup(
    name="google_closure_fabric",
    version="0.0.1",
    author="Aleksandr Batsuev",
    author_email="batsuev@gmail.com",
    description="TODO",
    license="BSD",
    keywords="google closure gjslint google_closure",
    url="https://github.com/batsuev/google-closure-fabric",
    packages=['google_closure_fabric'],
    long_description='TODO',
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