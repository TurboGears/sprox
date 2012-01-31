#setup.py
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
execfile(os.path.join(here, 'sprox', 'release.py'))

setup(
  name="sprox",
  version=__version__,
  zip_safe=False,
  include_package_data=True,
  description="""A package for creation of web widgets directly from database schema.""",
  author="Christopher Perkins 2007-2009 major contributions by Michael Brickenstein",
  author_email="chris@percious.com",
  license="MIT",
  url="http://www.sprox.org",
  install_requires=['tw.forms>=0.9.7.2',
                    'formencode>=1.2.2',
                    ],
  tests_require=['sqlalchemy'],
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
