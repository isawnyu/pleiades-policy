import unittest
from pleiades.policy.tests.base import PleiadesPolicyTestCase
from Products.CMFCore.utils import getToolByName


class TestNameCreation(PleiadesPolicyTestCase):

    def afterSetUp(self):
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.features = self.portal['features']
        self.features.manage_addLocalRoles('member', ['Contributor'])
        self.acl_users._doAddUser('member', 'secret', ['Member',],[])
        self.setRoles(('Manager',))
        self.workflow.doActionFor(self.features, 'submit')
        self.workflow.doActionFor(self.features, 'publish')

    def test_create_feature(self):
        self.login('member')
        fid = self.features.invokeFactory(
                'Feature',
                'foo bar',
                title=u'Foo Bar',
                featureType='settlement'
                )
        feature = self.features[fid]
        self.assertEquals(u'Foo Bar', feature.title)

        # and deletion
        self.features.manage_delObjects([fid])
        self.assert_(fid not in self.features.keys())
        

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestNameCreation))
    return suite
