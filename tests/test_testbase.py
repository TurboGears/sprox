from sprox.test.base import eq_xml, in_xml, fix_xml


def test_fix_xml():
    s = """<form action="" method="post" class="required tableform">
        <div></div>
        </form>"""
    e = """<form action="" class="required tableform" method="post"><div /></form>"""
    r =fix_xml(s)
    assert r == e, r
