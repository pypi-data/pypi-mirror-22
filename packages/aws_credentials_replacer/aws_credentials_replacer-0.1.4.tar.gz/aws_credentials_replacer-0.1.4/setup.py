#!/usr/bin/env python

from setuptools import setup

required = [
    'credstash',
    'jinja2',
    'click'
]

setup(
    name='aws_credentials_replacer',
    version='0.1.4',
    description='AWS credentials replacer',
    author='Anton Prokhorov',
    author_email='betrayer11@gmail.com',
    url='https://github.com/singleton11/aws-credential-replacer',
    packages=['credentials_replacer'],
    install_requires=required,
)
