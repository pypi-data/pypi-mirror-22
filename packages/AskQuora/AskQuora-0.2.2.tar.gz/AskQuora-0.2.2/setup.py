#!/usr/bin/python

from setuptools import setup, find_packages
import sys
import os
import askquora

setup(name='AskQuora',
      version='0.2.2',
      description='Quora Q&A right from the command line!',
      author='Ritiek Malhotra',
      author_email='ritiekmalhotra123@gmail.com',
      packages = find_packages(),
      entry_points={
            'console_scripts': [
                  'askquora = askquora.askquora:cli',
            ]
      },
      url='https://www.github.com/Ritiek/AskQuora',
      keywords=['quora', 'terminal', 'command-line', 'question', 'python'],
      license='MIT',
      download_url='https://github.com/Ritiek/AskQuora/archive/v0.2.2.tar.gz',
      classifiers=[],
      install_requires=[
            'requests',
            'BeautifulSoup4',
            'colorama',
            'requests-cache'
      ]
     )

