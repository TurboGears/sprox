from __future__ import absolute_import
from nose.tools import eq_
from sprox.widgets import ContainerWidget
from sprox.test.base import setup_database

def setup():
    setup_database()

class TestContainerWidget:
    def setup(self):
        self.widget = ContainerWidget()

    def test_createObj(self):
        pass

    def test_display(self):
        s = self.widget.render()
        assert 'class="containerwidget"' in s