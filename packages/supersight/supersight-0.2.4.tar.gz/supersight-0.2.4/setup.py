# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='supersight',
    version='0.2.4',
    description='A static website generator for MatplotLib plots',
    long_description=readme,
    author='Camille Moatti',
    author_email='camille.moatti@gmail.com',
    url='https://github.com/CamilleMo/SuperSight',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        "Jinja2",
    ],
    include_package_data = True
)

