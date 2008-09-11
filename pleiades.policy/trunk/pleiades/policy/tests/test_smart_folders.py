import unittest
from zope.component import getMultiAdapter
from zope.publisher.browser import TestRequest
from pleiades.policy.tests.base import PleiadesPolicyTestCase
from Products.CMFCore.utils import getToolByName


class TestSmartFolderCreation(PleiadesPolicyTestCase):

    def afterSetUp(self):
        self.places = self.portal['places']
        self.features = self.portal['features']
        self.names = self.portal['names']
        self.request = TestRequest()

    def test_create_collections(self):
        self.setRoles(('Manager',))
        view = getMultiAdapter(
                (self.places, self.request), 
                name=u'create-collections'
                )
        self.assert_(view() == 1)
        self.assert_('roman' in self.places)
        self.assert_('settlement' in self.places)
        
        topic = self.places['roman']
        c1 = topic['crit__getTimePeriods_ATSimpleStringCriterion']
        self.assertEqual(u'roman', c1.value)
        
        topic = self.places['settlement']
        c1 = topic['crit__getFeatureType_ATSimpleStringCriterion']
        self.assertEqual(u'settlement', c1.value)

        nid = self.names.invokeFactory(
                'Name',
                nameTransliterated='Foo'
                )
        name = self.names[nid]
        tid = name.invokeFactory(
                'TemporalAttestation',
                id='roman',
                timePeriod='roman',
                attestationConfidence='certain',
                )
        name.reindexObject()

        fid = self.features.invokeFactory(
                'Feature',
                title='A Feature',
                featureType='settlement',
                )
        feature = self.features[fid]
        feature.addReference(name, 'hasName')
        feature.reindexObject()

        pid = self.places.invokeFactory(
                'Place',
                title='A Place',
                )
        place = self.places[pid]
        place.addReference(feature, 'hasFeature')
        place.reindexObject()

        self.assertEquals(['settlement'], place.getFeatureType())
        self.assertEquals(['roman'], place.getTimePeriods())

        self.assertEquals([place.UID()], [b.UID for b in self.places['settlement'].queryCatalog()])
        self.assertEquals([place.UID()], [b.UID for b in self.places['roman'].queryCatalog()])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSmartFolderCreation))
    return suite
