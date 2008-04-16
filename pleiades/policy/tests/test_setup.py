import unittest
from pleiades.policy.tests.base import PleiadesPolicyTestCase

class TestSetup(PleiadesPolicyTestCase):
    
    def test_portal_title(self):
        self.assertEquals("Optilux Cinemas", self.portal.getProperty('title'))
        
    def test_portal_description(self):
        self.assertEquals("Welcome to Optilux Cinemas", self.portal.getProperty('description'))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
