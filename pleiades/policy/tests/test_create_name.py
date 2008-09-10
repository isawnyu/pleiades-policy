import unittest
from pleiades.policy.tests.base import PleiadesPolicyTestCase
from Products.CMFCore.utils import getToolByName


class TestNameCreation(PleiadesPolicyTestCase):

    def afterSetUp(self):
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.names = self.portal['names']
        self.locations = self.portal['locations']
        self.names.manage_addLocalRoles('member', ['Contributor'])
        self.locations.manage_addLocalRoles('member', ['Contributor'])
        self.acl_users._doAddUser('member', 'secret', ['Member',],[])
        self.setRoles(('Manager',))
        self.workflow.doActionFor(self.names, 'submit')
        self.workflow.doActionFor(self.names, 'publish')
        self.workflow.doActionFor(self.locations, 'submit')
        self.workflow.doActionFor(self.locations, 'publish')

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

        name.invokeFactory(
            'SecondaryReference',
            id='foo',
            title='foo',
            )
        self.assertEquals('foo', name['foo'].Title())

    def test_create_location(self):
        self.login('member')
        lid = self.locations.invokeFactory(
                'Location',
                geometry='Point: [0.0, 0.0]',
                )
        location = self.portal['locations'][lid]
        self.assertEquals('Point: [0.0, 0.0]', location.getGeometry())

        # and deletion
        self.locations.manage_delObjects([lid])
        self.assert_(lid not in self.locations.keys())

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestNameCreation))
    return suite
