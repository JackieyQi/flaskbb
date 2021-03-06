# -*- coding: utf-8 -*-
"""
    flaskbb.plugins.portal
    ~~~~~~~~~~~~~~~~~~~~~~

    A Portal Plugin for FlaskBB.

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
print "yjl file name:",__name__
from flask_plugins import connect_event

from flaskbb.plugins import FlaskBBPlugin
from flaskbb.utils.populate import (create_settings_from_fixture,
                                    delete_settings_from_fixture)
from flaskbb.forum.models import Forum

from .views import portal, inject_portal_link

__plugin__ = "PortalPlugin"


def available_forums():
    forums = Forum.query.order_by(Forum.id.asc()).all()
    return [(forum.id, forum.title) for forum in forums]


fixture = (
    ('plugin_portal', {
        'name': "Portal Settings",
        "description": "Configure the portal",
        "settings": (
            ('plugin_portal_forum_ids', {
                'value': [1],
                'value_type': "selectmultiple",
                'name': "Forum IDs",
                'description': ("The forum ids from which forums the posts "
                                "should be displayed on the portal."),
                'extra': {"choices": available_forums, "coerce": int}
            }),
            ('plugin_portal_recent_topics', {
                'value': 10,
                'value_type': "integer",
                'name': "Number of Recent Topics",
                'description': "The number of topics in Recent Topics.",
                'extra': {"min": 1},
            }),
        ),
    }),
)


class PortalPlugin(FlaskBBPlugin):
    settings_key = 'plugin_portal'

    def setup(self):
        self.register_blueprint(portal, url_prefix="/portal")
        connect_event("before-first-navigation-element", inject_portal_link)

    def install(self):
        create_settings_from_fixture(fixture)

    def uninstall(self):
        delete_settings_from_fixture(fixture)
