from sprox.configbase import ConfigBase, ConfigBaseError
from sprox.test.base import setup_database, sorted_user_columns, SproxTest, setup_records, Example, Document
from sprox.test.model import User, Town
import os.path
from nose.tools import raises, eq_
from nose.util import anyp, getpackage, test_address, resolve_name, src, tolist

import inspect
import doctest

import unittest

from nose.plugins import doctests as nose_doctest

from sprox import configbase, fillerbase, formbase, saormprovider, sprockets, tablebase, metadata, validators, validatorselector, widgets, widgetselector
from sprox.dojo import formbase as dojo_formbase

import sprox

session = None
engine  = None
connection = None
trans = None
metadata = None
def setup():
    global session, engine, metadata, trans
    session, engine, metadata = setup_database()
    user = setup_records(session)
    #this may be needed if we end up testing the provider with doctests
    #session.commit()
    
def teardown():
    session.rollback()

def test_doctests():
    global session, metadata
    import unittest
    import doctest
    
    def setUp(self):
        #this may be needed if we end up testing the provider with doctests
        pass
    def tearDown(self):
        #this may be needed if we end up testing the provider with doctests
        #session.rollback()
        pass
    suite = unittest.TestSuite()
    for mod in dir(sprox):
        mod = getattr(sprox, mod)
        if inspect.ismodule(mod):
            try:
                suite.addTest(doctest.DocTestSuite(mod, globs={'session':session, 'User': User, 'Town':Town, 'metadata':metadata}, setUp=setUp, tearDown=tearDown))
            except ValueError:
                pass
    suite.addTest(doctest.DocTestSuite(dojo_formbase, globs={'session':session, 'User': User, 'Town':Town, 'metadata':metadata}, setUp=setUp, tearDown=tearDown))

    runner = unittest.TextTestRunner()
    runner.run(suite)
