import unittest

import zope.component
import zope.interface

from Zope2.App import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc

from pmr2.users.interfaces import IEmailManager
from pmr2.users.browser import UserEmailForm

from pmr2.testing.base import TestRequest
from pmr2.users.tests import base


class EmailEditorTestCase(ptc.PloneTestCase):
    """
    For the browser side of things.
    """

    def afterSetUp(self):
        self.portal.acl_users._doAddUser('user1', 'secret', ['Member'], [])
        self.portal.acl_users._doAddUser('user2', 'secret', ['Member'], [])
        self.email_manager = zope.component.getAdapter(
            self.portal, IEmailManager)

    def test_user_email_form_render(self):
        context = self.portal
        request = TestRequest()
        form = UserEmailForm(context, request)
        result = form()
        self.assertTrue('<textarea' in result)

    def test_user_email_set(self):
        self.login('user1')
        context = self.portal
        request = TestRequest(form={
            'form.widgets.addresses': 'user1@example.com\nuser11@example.com',
            'form.buttons.apply': 1,
        })
        form = UserEmailForm(context, request)
        result = form()
        self.assertEqual(self.email_manager.get_emails_for('user1'), [
            u'user11@example.com',
            u'user1@example.com',
        ])

        self.login('user2')
        context = self.portal
        request = TestRequest(form={
            'form.widgets.addresses': 'user1@example.com\nuser22@example.com',
            'form.buttons.apply': 1,
        })
        form = UserEmailForm(context, request)
        result = form()
        self.assertEqual(self.email_manager.get_emails_for('user2'), [
            u'user22@example.com',
        ])
