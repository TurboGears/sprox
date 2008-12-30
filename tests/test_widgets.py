from sprox.widgets import SproxCheckBox
from nose.tools import raises, eq_

class TestSproxCheckbox:
    def setup(self):
        self.widget = SproxCheckBox()

    def test_checkbox_invalid_data(self):
        self.widget(value = 'asdf')