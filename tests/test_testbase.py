from sprox.test.base import eq_xml, in_xml, fix_xml


def test_fix_xml():
    s = """<form action="" method="post" class="required tableform">
        <div></div>
        </form>"""
    r = fix_xml(s)
    assert '><div /></form>' in r, r


def test_fix_xml_with_escapes():
    s = """<form action="" method="post" class="required tableform">
        <div></div>&nbsp;
        </form>"""
    r = fix_xml(s)
    assert '><div /></form>' in r, r

def test_fix_xml_with_namespace():
    s = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <body>
    <form action="" method="post" class="required tableform">
        <div></div>&nbsp;
        </form>
    </body>
    </html>"""
    r = fix_xml(s)
    # assert '><div /></form></body></html>' in r, r
    # TODO: should namespace be removed? r is:
    # <html:html xmlns:html="http://www.w3.org/1999/xhtml"><body><html:form action="" class="required tableform" method="post"><html:div /></html:form></body></html:html>

