import zope.interface
import zope.schema
from zope.component.hooks import getSite
import z3c.form.field
import z3c.form.button

from Products.CMFCore.utils import getToolByName

from pmr2.z3cform import form

from pmr2.users.interfaces import IEmailManager


class IUserEmail(zope.interface.Interface):

    addresses = zope.schema.Text(
        title=u'Your alternative email addresses',
        description=u'Enter alternative email addresses that you own that '
            'you want to be referenced by the commits in the history with.',
    )


@zope.interface.implementer(IUserEmail)
class UserEmail(object):

    addresses = zope.schema.fieldproperty.FieldProperty(
        IUserEmail['addresses'])


class UserEmailForm(form.EditForm):

    fields = z3c.form.field.Fields(IUserEmail)

    label = "Extra user information editor"

    def update(self):
        self.request['disable_border'] = True
        super(UserEmailForm, self).update()

    def _getLoginAndManager(self):
        site = getSite()
        mt = getToolByName(site, 'portal_membership')
        login = mt.getAuthenticatedMember().id
        email_manager = zope.component.getAdapter(site, IEmailManager)
        return login, email_manager

    def getContent(self):
        site = getSite()
        result = UserEmail()

        login, email_manager = self._getLoginAndManager()

        result.addresses = u'\n'.join(email_manager.get_emails_for(login))

        return result

    @z3c.form.button.buttonAndHandler(u'Apply', name='apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        if changes:
            self.status = self.successMessage
            login, email_manager = self._getLoginAndManager()
            email_manager.set_email(login, data['addresses'].splitlines())
        else:
            self.status = self.noChangesMessage
