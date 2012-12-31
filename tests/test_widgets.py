from sprox.widgets import SproxCheckBox, PropertyMultipleSelectField
from nose.tools import raises, eq_
from formencode.validators import Int as IntValidator

class TestSproxCheckbox:
    def setup(self):
        self.widget = SproxCheckBox()

    def test_checkbox_invalid_data(self):
        self.widget.display(value = 'asdf')

class TestMultipleSelection:
    def setup(self):
        self.widget = PropertyMultipleSelectField(options=[('1', 'a'), ('2', 'b')],
                                                  validator=IntValidator())

    def test_multiple_selection_single_entry(self):
        self.widget.req()._validate('1') == [1]

    def test_multiple_selection_invalid_entries(self):
        self.widget.req()._validate(['a', 'b']) == []