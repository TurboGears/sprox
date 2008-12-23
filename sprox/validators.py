"""
validators Module

Copyright (c) 2008 Christopher Perkins
Original Version by Christopher Perkins 2008
Released under MIT license.
"""
from formencode import FancyValidator, Invalid

class UniqueValue(FancyValidator):
    def __init__(self, provider, field, *args, **kw):
        self.provider = provider
        self.field    = field
        FancyValidator.__init__(self, *args, **kw)

    def _to_python(self, value, state):
        if not self.provider.is_unique(self.field, value):
            raise Invalid(
                'That value already exists',
                value, state)
        return value

