import os

from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

def read(f_name):
    return open(os.path.join(os.path.dirname(__file__), f_name), encoding="utf8").read()

setup(
    name="tourist-bot",
    version="1.0.0",
    author_email="Egor Rassokhin, Boris Suhomlin, Roman Uraykin",
    description="Events, news, and places poster",
    long_description=read("README.md"),
    package_data={'': ['*']},
    install_requires=requirements,
    include_package_data=True
)