# -*- coding: utf-8 -*-
from cgi import escape
from uuid import uuid1


class AlfredItemsList(object):
    def __init__(self, items=None):
        self.items = items or []
        self.pattern = \
            u'<item arg="{arg}" uid="{uid}" valid="{valid}">"' + \
            u'<title>{title}</title>' + \
            u'<subtitle>{subtitle}</subtitle>' + \
            u'<icon>icon.png</icon>' + \
            u'</item>'

    def append(
            self,
            arg,
            title,
            subtitle,
            valid=u'yes',
            icon=u'icon',
            uid=None
        ):
        """Use uid = None to preserve order of items"""
        uid = uid or str(uuid1())
        # using uuid is little hacky, there is no other way to
        # prevent alfred from reordering items
        self.items.append(
            (arg, escape(title), escape(subtitle), valid, icon, uid)
        )

    def to_ustr(self):
        # for arg, title, subtitle, valid, icon, uid in self.items:
        items = u"".join(
            [self.pattern.format(
                arg=arg,
                title=title.decode('utf-8'),
                subtitle=escape(subtitle),
                valid=valid,
                icon=icon,
                uid=uid,
                ) for arg, title, subtitle, valid, icon, uid in self.items
            ]
        )
        return u'<items>' + items + u'</items>'

    def __add__(self, other):
        return AlfredItemsList(self.items + other.items)
