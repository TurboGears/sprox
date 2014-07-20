try: #pragma: no cover
    from .tw2widgets.widgets import *
except ImportError: #pragma: no cover
    from .tw1widgets.widgets import *

try: #pragma: no cover
    from tw2.forms import CalendarBase
except: #pragma: no cover
    class CalendarBase(object):
        pass
