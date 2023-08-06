#!/usr/bin/env python3

from setuptools import setup

__version__ = '1.00'

setup(name='vdgalcon',
      version=__version__,
      install_requires='visidata requests'.split(),
      description='Galactic Conquest in curses, on VisiData',
      long_description=open('README.md').read(),
      author='Saul Pwanson',
      author_email='vdgalcon@saul.pw',
      url='http://github.com/saulpw/vdgalcon',
      download_url='https://github.com/saulpw/vdgalcon/tarball/' + __version__,
      scripts=['vdgalcon.py', 'vdgalcon-server.py'],
      license='GPLv3',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Environment :: Console :: Curses',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Topic :: Office/Business :: Financial :: Spreadsheet',
      ],
      keywords=('console game textpunk visidata galactic conquest galcon')
      )
