"""Insta485 python package configuration."""

from setuptools import setup

setup(
    name='insta485',
    version='0.1.0',
    packages=['insta485'],
    include_package_data=True,
    install_requires=[
        'Flask==0.12.2',
        'html5validator==0.2.8',
        'pycodestyle==2.3.1',
        'pydocstyle==2.0.0',
        'pylint==1.8.1',
        'arrow==0.10.0',
        'sh==1.12.14',
    ],
)
