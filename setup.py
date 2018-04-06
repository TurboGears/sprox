#setup.py
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
exec(compile(open(os.path.join(here, 'sprox', 'release.py')).read(), 'release.py', 'exec'), globals(), locals())

import sys
py_version = sys.version_info[:2]

DEPENDENCIES = ['formencode>=1.3.0a1']
TESTS_DEPENDENCIES = ['sieve']

if py_version == (3, 2):
    DEPENDENCIES += ['markupsafe<0.16']
    TESTS_DEPENDENCIES.append('coverage < 4.0')
else:
    DEPENDENCIES += ['markupsafe']
    TESTS_DEPENDENCIES.append('coverage')

if py_version == (2, 6):
    TESTS_DEPENDENCIES.append('sqlalchemy < 1.2')
    TESTS_DEPENDENCIES.append('ming < 0.5.6')
else:
    TESTS_DEPENDENCIES.append('sqlalchemy')
    TESTS_DEPENDENCIES.append('ming')


TEST_SUITE_DEPENDENCIES = TESTS_DEPENDENCIES + ['tw2.forms', 'genshi', 'mako']

setup(
  name="sprox",
  version=__version__,
  zip_safe=False,
  include_package_data=True,
  description="""A package for creation of web widgets directly from database schema.""",
  author="Christopher Perkins, Michael Brickenstein, Alessandro Molina",
  author_email="chris@percious.com, amol@turbogears.org",
  license="MIT",
  url="http://www.sprox.org",
  install_requires=DEPENDENCIES,
  tests_require=TESTS_DEPENDENCIES,
  extras_require={
       # Used by Travis and Coverage due to setup.py nosetests
       # causing a coredump when used with coverage
       'testing': TEST_SUITE_DEPENDENCIES,
  },
  packages = find_packages(),
  classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
 entry_points = """[toscawidgets]
        # Use 'widgets' to point to the module where widgets should be imported
        # from to register in the widget browser
        widgets = sprox.widgets
        # Use 'samples' to point to the module where widget examples
        # should be imported from to register in the widget browser
        # samples = tw.samples
        # Use 'resources' to point to the module where resources
        # should be imported from to register in the widget browser
        #resources = sprox.widgets.resources
       """
#  entry_points="""
#        [paste.paster_create_template]
#        dbsprockets=sprox.instance.newSprox:Template
#    """,

  )
