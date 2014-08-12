from persistent import Persistent
from persistent.list import PersistentList
from BTrees.OOBTree import OOBTree

from zope.container.contained import Contained
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.annotation import factory

from zope.schema import fieldproperty
import zope.component


@zope.component.adapter(IAttributeAnnotatable)
class EmailManager(Persistent, Contained):
    """
    Alternative email tracker

    This tracks the alternative email addresses that a user may possess
    and this provides the methods to track and retrieve them.

    Does not provide any robust error checking.
    """

    def __init__(self):
        # for looking up an email address to a login
        self._email_to_login = OOBTree()
        # for tracking users' own email addresses
        self._user_email_lists = OOBTree()

    def set_email(self, login, emails):
        self.del_email(login)
        # we emptied the entire old list anyway...
        self._user_email_lists[login] = email_list = PersistentList()
        self._add_email(login, *emails)

    def add_email(self, login, email):
        email_list = self._user_email_lists.get(login, None)
        if email_list is None:
            self._user_email_lists[login] = email_list = PersistentList()

        self._add_email(login, email)

    def _add_email(self, login, *emails):
        """
        This is the one and only method that could add data to both

        - self._email_to_login  (via append)
        - self._user_email_lists  (via set)
        """

        email_list = self._user_email_lists[login]
        for email in emails:
            current_owner = self.get_login_for(email) 
            if not current_owner is None:
                if email in self.get_emails_for(current_owner):
                    # silently fail
                    continue
            email_list.append(email)
            self._email_to_login[email] = login

    def del_email(self, login, *emails):
        email_list = self._user_email_lists.get(login, ())
        if not email_list:
            return

        if not emails:
            # remove all user's email addresses.
            emails = list(email_list)

        for email in emails:
            try:
                self._email_to_login.pop(email, None)
                email_list.remove(email)
            except ValueError:
                pass

    def get_emails_for(self, login):
        """
        Return all emails for this login.
        """

        return sorted(self._user_email_lists.get(login, []))

    def get_login_for(self, email):
        """
        Return the login for this email address.
        """

        return self._email_to_login.get(email, None)

EmailManagerFactory = factory(EmailManager)
