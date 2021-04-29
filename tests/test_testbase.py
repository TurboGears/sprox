from sprox.test.base import eq_xml, in_xml, fix_xml
from sys import version_info

# unordered attrs (python<3.8) are somewhat consistent anyway
attrs_order_kept = version_info[0] >= 3 and version_info[1] >= 8

def test_fix_xml():
    s = """<form action="" method="post" class="required tableform">
        <div></div>
        </form>"""
    if attrs_order_kept:
        e = """<form action="" method="post" class="required tableform"><div /></form>"""
    else:
        e = """<form action="" class="required tableform" method="post"><div /></form>"""
    r = fix_xml(s)
    assert r == e, (r, e)

def test_fix_xml_with_escapes():
    s = """<form action="" method="post" class="required tableform">
        <div></div>&nbsp;
        </form>"""
    if attrs_order_kept:
        e = """<form action="" method="post" class="required tableform"><div /></form>"""
    else:
        e = """<form action="" class="required tableform" method="post"><div /></form>"""
    r = fix_xml(s)
    assert r == e, (r, e)

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
    e = """<html><body><form action="" class="required tableform" method="post"><div /></form></body></html>"""
    r = fix_xml(s)
