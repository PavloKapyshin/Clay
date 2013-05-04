# -*- coding: utf-8 -*-
from clay.tglobals import active

from .helpers import *


def setup_module():
    remove_test_dirs()
    make_dirs(SOURCE_DIR)


def teardown_module():
    remove_test_dirs()


ACTIVE_PATH = '/foo/bar/'


def _test_active():
    assert not active('/hello/')
    assert active(ACTIVE_PATH) == 'active'
    assert active('/hello/', ACTIVE_PATH[:5], partial=True) == 'active'
    assert active('/hello/', ACTIVE_PATH) == 'active'
    assert not active('/hello/', '/world/')


def _test_active_relative():
    assert not active('meh')
    assert active('bar') == 'active'
    assert active('b', partial=True) == 'active'


def _test_active_patterns():
    assert active('/*/bar') == 'active'
    assert active('/fo?/bar') == 'active'
    assert active('/f*') == 'active'


def _test_active_backward_compatibilty():
    assert active(['/hello/', ACTIVE_PATH,]) == 'active'
    assert not active(['/hello/', '/world/',])
    assert active([ ACTIVE_PATH[:5] ], partial=True) == 'active'


def test_active(c):
    with c.app.test_request_context(ACTIVE_PATH, method='GET'):
        _test_active()


def test_active_relative(c):
    with c.app.test_request_context(ACTIVE_PATH, method='GET'):
        _test_active_relative()


def test_active_patterns(c):
    with c.app.test_request_context(ACTIVE_PATH, method='GET'):
        _test_active_patterns()


def test_active_backward_compatibilty(c):
    with c.app.test_request_context(ACTIVE_PATH, method='GET'):
        _test_active_backward_compatibilty()


def test_active_in_templates(t):
    setup_module()
    make_dirs(SOURCE_DIR)

    path = 'bbbb.html'
    content = u'''class="{{ active('%s') }}"''' % path
    create_file(get_source_path(path), content)

    expected = u'class="active"'
    resp = t.get('/' + path)
    assert resp.data == expected

