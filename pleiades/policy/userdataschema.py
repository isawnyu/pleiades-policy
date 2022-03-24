from zope.interface import implements
from zope.schema import URI
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEnhancedUserDataSchema


class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """

    viaf_link = URI(title=u'VIAF profile Link', required=False)
    orcid_link = URI(title=u'ORCID profile Link', required=False)
    twitter_link = URI(title=u'Twitter link', required=False)
    facebook_link = URI(title=u'Facebook link', required=False)
    academia_link = URI(title=u'Academia.edu link', required=False)
    linkedin_link = URI(title=u'LinkedIn link', required=False)
    employer_link = URI(title=u'Institutional/Employer web page link', required=False)


def memberURIAttribute(name):
    def getter(self):
        return self._getProperty(name)

    def setter(self, value):
        if value is None:
            value = ''
        return self.context.setMemberProperties({name: value})

    return property(getter, setter)


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """Personal preferences adapter that includes member uris
    """
    viaf_link = memberURIAttribute('viaf_link')
    orcid_link = memberURIAttribute('orcid_link')
    twitter_link = memberURIAttribute('twitter_link')
    facebook_link = memberURIAttribute('facebook_link')
    academia_link = memberURIAttribute('academia_link')
    linkedin_link = memberURIAttribute('linkedin_link')
    employer_link = memberURIAttribute('employer_link')


class MemberLinksView(BrowserView):

    def links(self, userid):
        mtool = getToolByName(self.context, 'portal_membership')
        user = mtool.getMemberById(userid)
        return {
            'viaf_link': user.getProperty('viaf_link', None),
            'orcid_link': user.getProperty('orcid_link', None),
            'twitter_link': user.getProperty('twitter_link', None),
            'facebook_link': user.getProperty('facebook_link', None),
            'academia_link': user.getProperty('academia_link', None),
            'linkedin_link': user.getProperty('linkedin_link', None),
            'employer_link': user.getProperty('employer_link', None),
        }
