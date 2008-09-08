import unittest
from pleiades.policy.tests.base import PleiadesPolicyTestCase
from Products.CMFCore.utils import getToolByName


class TestNameCreation(PleiadesPolicyTestCase):

    def afterSetUp(self):
        self.portal.error_log._ignored_exceptions = ()
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.names = self.portal['names']
        self.names.manage_addLocalRoles('member', ['Contributor'])
        self.acl_users._doAddUser('member', 'secret', ['Member',],[])
        self.setRoles(('Manager',))
        self.workflow.doActionFor(self.names, 'submit')
        self.workflow.doActionFor(self.names, 'publish')

    def test_create_name(self):
        self.login('member')
        nameTransliterated = u'Foo Bar'
        nid = self.names.invokeFactory(
                'Name',
                title=nameTransliterated.encode('utf-8'),
                nameTransliterated=nameTransliterated.encode('utf-8'),
                nameAttested=u'',
                nameLanguage=u''
                )
        name = self.portal['names'][nid]
        self.assertEquals(u'Foo Bar', name.nameTransliterated)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestNameCreation))
    return suite
