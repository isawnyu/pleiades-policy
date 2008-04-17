import unittest
from pleiades.policy.tests.base import PleiadesPolicyTestCase
from Products.CMFCore.utils import getToolByName


class TestSetup(PleiadesPolicyTestCase):

    def afterSetUp(self):
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.types = getToolByName(self.portal, 'portal_types')
    
    def test_portal_title(self):
        self.assertEquals("Pleiades Beta Portal", self.portal.getProperty('title'))
        
    def test_portal_description(self):
        self.assertEquals("This is the beta portal for the Pleiades Project.", self.portal.getProperty('description'))

    def test_workflow_installed(self):
        self.failUnless('pleiades_entity_workflow' in self.workflow.objectIds())
        
    def test_workflows_mapped(self):
        self.assertEquals(('pleiades_entity_workflow',), self.workflow.getDefaultChain())
        for portal_type, chain in self.workflow.listChainOverrides():
            if portal_type in ('File', 'Image',):
                self.assertEquals(('pleiades_entity_workflow',), chain)
        
    def test_view_permisison_for_staffmember(self):
        # The API of the permissionsOfRole() function sucks - it is bound too
        # closely up in the permission management screen's user interface
        self.failUnless('View' in [r['name'] for r in 
                                self.portal.permissionsOfRole('Reader') if r['selected']])

    def test_structure(self):
        self.failUnless('disclaimer' in self.portal.keys())
        self.failUnless('front-page' in self.portal.keys())
        self.failUnless('about-pleiades' in self.portal.keys())
        self.failUnless('names' in self.portal.keys())
        self.failUnless('locations' in self.portal.keys())
        self.failUnless('places' in self.portal.keys())

    def test_vocabulary_installed(self):
        self.failUnless('vocabulary' in self.portal.keys())
        skins = getToolByName(self.portal, 'portal_skins')
        layer = skins.getSkinPath('Pleiades Vocabulary')
        self.failUnless('pleiades_vocabulary_custom_templates' in layer)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite