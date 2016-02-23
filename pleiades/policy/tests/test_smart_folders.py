from zope.component import getMultiAdapter
from zope.publisher.browser import TestRequest
from pleiades.policy.tests.base import PleiadesPolicyTestCase


class TestSmartFolderCreation(PleiadesPolicyTestCase):

    def afterSetUp(self):
        self.places = self.portal['places']
        self.features = self.portal['features']
        self.setRoles(('Manager',))
        self.portal.invokeFactory(
            'Folder',
            'collections',
            title='Collections',
        )
        self.collections = self.portal['collections']
        self.request = TestRequest()

    def test_create_collections(self):
        self.setRoles(('Manager',))
        view = getMultiAdapter(
            (self.collections, self.request),
            name=u'create-collections'
        )
        self.assert_(view() == 1)
        self.assert_('roman' in self.collections)
        self.assert_('settlement' in self.collections)

        topic = self.collections['roman']
        c1 = topic['crit__getTimePeriods_ATSimpleStringCriterion']
        self.assertEqual(u'roman', c1.value)

        topic = self.collections['settlement']
        c1 = topic['crit__getFeatureType_ATSimpleStringCriterion']
        self.assertEqual(u'settlement', c1.value)

        pid = self.places.invokeFactory(
            'Place',
            '0',
            title='A Place',
            placeType=['settlement'],
        )
        place = self.places[pid]
        nid = place.invokeFactory(
            'Name',
            'foo',
            nameTransliterated='Foo'
        )
        name = place[nid]
        attestations = name.Schema()['attestations']
        attestations.resize(1)
        name.update(attestations=[dict(confidence='certain', timePeriod='roman')])
        place.reindexObject()

        self.assertEquals(['settlement'], place.getFeatureType())
        self.assertEquals(['roman'], place.getTimePeriods())

        self.assertEquals([place.UID()], [b.UID for b in self.collections['settlement'].queryCatalog()])
        self.assertEquals([place.UID()], [b.UID for b in self.collections['roman'].queryCatalog()])
