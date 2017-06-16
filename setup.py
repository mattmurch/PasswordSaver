#!/usr/bin/env python3

from setuptools import setup

__version__ = '1.00'

setup(name='PasswordSaver',
      version=__version__,
      install_requires=['bcrypt>=3.1.3',
					'cryptography>=1.8.1',
					'SQLAlchemy>=1.1.9',
					'visidata==0.61'],
      description='local encrypted database application for remembering usernames and passwords',
      long_description=open('README.md').read(),
      author='Matt Murch',
      author_email='mattmurch@gmail.com',
      url='https://github.com/mattmurch/PasswordSaver',
      download_url='https://github.com/mattmurch/PasswordSaver/tarball/' + __version__,
      scripts=['password_saver.py'],
      license='MIT',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Topic :: Security :: Cryptography',
          'Topic :: Utilities',
      ],
      keywords=('password username login storage save saver secure encrypted'),
      packages=['models'],
      )
