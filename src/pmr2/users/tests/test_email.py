import unittest

from pmr2.users.email import EmailManager


class EmailManagerTestCase(unittest.TestCase):
    """
    Test case for the EmailManager
    """

    def setUp(self):
        self.email_manager = EmailManager()

    def test_basic(self):
        self.assertEqual(
            self.email_manager.get_login_for('testuser@example.com'), None)

    def test_add_basic(self):
        self.email_manager.add_email('testuser', 'testuser@example.org')
        self.email_manager.add_email('testuser', 'testuser@example.com')
        self.email_manager.add_email('manager', 'manager@example.net')

        testuser_emails = self.email_manager.get_emails_for('testuser')
        self.assertEqual(testuser_emails,
            ['testuser@example.com', 'testuser@example.org'])

        self.assertEqual(
            self.email_manager.get_login_for('testuser@example.com'),
            'testuser'
        )

        self.assertEqual(
            self.email_manager.get_login_for('testuser@example.com'),
            'testuser'
        )

    def test_del_email(self):
        self.email_manager.set_email('a_user', [
            'testuser@example.org',
            'a_user@example.com',
            'alternative@example.com',
            'extra@example.com',
        ])

        self.email_manager.del_email('a_user', 'extra@example.com')
        self.assertEqual(self.email_manager.get_emails_for('a_user'), [
            'a_user@example.com',
            'alternative@example.com',
            'testuser@example.org',
        ])
        self.assertNotEqual(
            self.email_manager.get_login_for('extra@example.com'), 'a_user')

        self.email_manager.del_email('a_user')
        self.assertEqual(self.email_manager.get_emails_for('a_user'), [])
        self.assertNotEqual(
            self.email_manager.get_login_for('a_user@example.com'), 'a_user')

    def test_add_multi(self):
        self.email_manager.set_email('a_user', [
            'testuser@example.org',
            'a_user@example.com',
            'alternative@example.com',
        ])

        testuser_emails = self.email_manager.get_emails_for('a_user')
        self.assertEqual(testuser_emails, [
            'a_user@example.com',
            'alternative@example.com',
            'testuser@example.org',
        ])

        self.assertEqual(
            self.email_manager.get_login_for('a_user@example.com'), 'a_user')

        self.email_manager.set_email('a_user', ['testuser@example.com',])

        testuser_emails = self.email_manager.get_emails_for('a_user')
        self.assertEqual(testuser_emails, ['testuser@example.com'])

        self.assertNotEqual(
            self.email_manager.get_login_for('a_user@example.com'), 'a_user')
        self.assertNotEqual(
            self.email_manager.get_login_for('alternative@example.com'),
            'a_user')

        self.assertEqual(
            self.email_manager.get_login_for('testuser@example.com'), 'a_user')

    def test_add_duplicated(self):
        # shouldn't error
        self.email_manager.add_email('testuser', 'testuser@example.org')
        self.email_manager.add_email('testuser', 'testuser@example.org')
        self.assertEqual(
            self.email_manager.get_login_for('testuser@example.org'),
            'testuser')

        self.assertEqual(self.email_manager.get_emails_for('testuser'), [
            'testuser@example.org'])

        # should have been ignored.
        self.email_manager.add_email('anotheruser', 'testuser@example.org')
        self.assertEqual(
            self.email_manager.get_login_for('testuser@example.org'),
            'testuser')

        self.assertEqual(self.email_manager.get_emails_for('anotheruser'), [])
        self.assertEqual(self.email_manager.get_emails_for('testuser'), [
            'testuser@example.org'])
