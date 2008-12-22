from sprox.entitiesbase import EntitiesBase
from base import setup_database
from nose.tools import raises, eq_
from model import User

session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, connection, trans
    session, engine, connection = setup_database()

class ModelsView(EntitiesBase):
    __entity__ = User

class TestViewBase:
    def setup(self):
        self.view = ModelsView(session)

    def test_create(self):
        pass

    def test__widget__(self):
        rendered = self.view.__widget__()
        assert """<div class="entitylabelwidget">
<a href="Visit/">Visit</a>
</div>""" in rendered, rendered