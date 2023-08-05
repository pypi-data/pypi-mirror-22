# -*- coding:utf-8 -*-

import os
import sys


from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.rst')) as f:
        README = f.read()
    with open(os.path.join(here, 'CHANGES.txt')) as f:
        CHANGES = f.read()
except IOError:
    README = CHANGES = ''


install_requires = [
    "dictknife[load]",
    "magicalimport",
    "jinja2",
    "colorama",
]


docs_extras = [
]

tests_require = [
]

testing_extras = tests_require + [
]

setup(name='zenmai',
      version='0.3.0',
      description='toy language on yaml or json',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: Implementation :: CPython",
      ],
      keywords='yaml, json, toylang, minilang',
      author="podhmo",
      author_email="ababjam61+github@gmail.com",
      url="https://github.com/podhmo/zenmai",
      packages=find_packages(exclude=["zenmai.tests"]),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require={
          'testing': testing_extras,
          'docs': docs_extras,
      },
      tests_require=tests_require,
      test_suite="zenmai.tests",
      entry_points="""
      [console_scripts]
      zenmai=zenmai.cmd:main
""")
