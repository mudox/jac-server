# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re

from setuptools import find_packages, setup

version = re.search(
    r"^__version__\s*=\s*'(.*)'",
    open('src/jacsrv/cmd.py').read(),
    re.M
).group(1)


setup(
    name='jacsrv',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    entry_points={
        "console_scripts": ['jacsrv = jacsrv.cmd:run']},
    version=version,
    description='TBD',
    long_description='TBD',
    author='Mudox',
    author_email='imudox@gmail.com',
    url='https://github.com/mudox/jacsrv'
)
