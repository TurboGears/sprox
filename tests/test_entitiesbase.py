from sprox.entitiesbase import EntitiesBase
from sprox.test.base import setup_database
from nose.tools import raises, eq_
from sprox.test.model import User

session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, metadata, trans
    session, engine, metadata = setup_database()

class ModelsView(EntitiesBase):
    __entity__ = User

class TestViewBase:
    def setup(self):
        self.view = ModelsView(session)

    def test_create(self):
        pass

    def test__widget__(self):
        rendered = self.view()
        assert """<div class="entitylabelwidget">
<a href="User/">User</a>
</div>""" in rendered, rendered