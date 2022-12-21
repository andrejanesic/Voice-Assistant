# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from distutils.core import setup


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='voice-assistant',
    version='0.1.0',
    description='Simple voice assistant built with deep learning models',
    long_description=readme,
    author='Luka Brcic, Andreja Nesic, Nikola Tadic',
    author_email='office@andrejanesic.com',
    url='https://github.com/ntadicrn4419/Voice-Assistant',
    license=license,
    packages=['voiceassistant', 'voiceassistant.test']
)
