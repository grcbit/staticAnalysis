# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
    (T('Analysis'), False, '#', [
        (T('App'), False, URL('default', 'aplicacion')),
        (T('Result'), False, URL('default', 'resultado')),
    ]),
    (T('License'), False, URL('default', 'licencia'), []),
]
