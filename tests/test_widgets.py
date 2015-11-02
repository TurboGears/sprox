from sprox.widgets import SproxCheckBox, PropertyMultipleSelectField, SproxMethodPutHiddenField
from nose import SkipTest
from formencode.validators import Int as IntValidator


class TestSproxCheckbox:
    def setup(self):
        self.widget = SproxCheckBox()

    def test_checkbox_invalid_data(self):
        self.widget.display(value = 'asdf')


class TestSproxMethodPUT:
    def setup(self):
        self.widget = SproxMethodPutHiddenField()

    def test_value(self):
        assert 'value="PUT"' in self.widget.display()

    def test_name(self):
        assert 'name="_method"' in self.widget.display()


class TestMultipleSelection:
    def setup(self):
        class FakeProvider(object):
            def get_dropdown_options(self, e, fn, dfn):
                return [('1', 'a'), ('2', 'b')]

        self.widget = PropertyMultipleSelectField(options=[('1', 'a'), ('2', 'b')],
                                                  validator=_ListOrIntValidator(),
                                                  item_validator=IntValidator(),
                                                  provider=FakeProvider())

    def test_multiple_selection_single_entry(self):
        if not hasattr(self.widget, 'req'):
            raise SkipTest('Test for Tw2')
        self.widget.req()._validate('1') == [1]

    def test_multiple_selection_invalid_entries(self):
        if not hasattr(self.widget, 'req'):
            raise SkipTest('Test for TW2')
        self.widget.req()._validate(['a', 'b']) == []

    def test_multiple_selection_invalid_entries_display(self):
        if not hasattr(self.widget, 'req'):
            raise SkipTest('Test for TW2')
        res = self.widget.req().display(value=['1', 'b', 'c', 'd', 'e'])
        res.count('selected="selected"') == 1, res


class _ListOrIntValidator(IntValidator):
    def _convert_to_python(self, value, state):
        if isinstance(value, list):
            return value
        super(_ListOrIntValidator, self)._convert_to_python(value)
