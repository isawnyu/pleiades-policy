from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from pleiades.vocabularies.vocabularies import get_vocabulary


class CreateCollections(BrowserView):

    def __call__(self):
        context = self.context
        atctool = getToolByName(context, 'portal_atct')
        vtool = getToolByName(context, 'portal_vocabularies')
        utils = getToolByName(context, 'plone_utils')

        try:
            atctool.removeIndex("getFeatureType")
        except:
            pass
        try:
            atctool.removeIndex("getTimePeriods")
        except:
            pass

        try:
            atctool.addIndex(
                'getFeatureType',
                'Place/Feature Type',
                'Type of ancient place or feature',
                enabled=True
                )
        except:
            pass
        try:
            atctool.addIndex(
                'getTimePeriods',
                'Time Periods',
                'Attested time periods',
                enabled=True
                )
        except:
            pass

        vocab_time = get_vocabulary('time_periods')
        vocab_type = vtool.getVocabularyByName('place-types')
        v_times = dict([(t['id'], t['title']) for t in vocab_time])
        v_types = dict(vocab_type.getDisplayList(self).items())

        # [time]/[type]
        for ko, vo in v_times.items():
            tid = context.invokeFactory(
                'Topic',
                id=utils.normalizeString(ko),
                title=vo
                )
            topic = context[tid]
            c = topic.addCriterion('getTimePeriods', 'ATSimpleStringCriterion')
            c.setValue(ko)
            c = topic.addCriterion('portal_type', 'ATPortalTypeCriterion')
            c.setValue('Place')
            topic.setSortCriterion('sortable_title', reversed=False)

            for ki, vi in v_types.items():
                sid = topic.invokeFactory(
                    'Topic',
                    id=utils.normalizeString(ki),
                    title=vi
                )
                subtopic = topic[sid]
                subtopic.setAcquireCriteria(True)
                c = subtopic.addCriterion(
                    'getFeatureType', 'ATSimpleStringCriterion'
                    )
                c.setValue(ki)
                subtopic.setSortCriterion('sortable_title', reversed=False)

        # [type]/[time]
        for ko, vo in v_types.items():
            tid = context.invokeFactory(
                'Topic',
                id=utils.normalizeString(ko),
                title=vo
            )
            topic = context[tid]
            c = topic.addCriterion('getFeatureType', 'ATSimpleStringCriterion')
            c.setValue(ko)
            c = topic.addCriterion('portal_type', 'ATPortalTypeCriterion')
            c.setValue('Place')
            topic.setSortCriterion('sortable_title', reversed=False)

            for ki, vi in v_times.items():
                sid = topic.invokeFactory(
                    'Topic',
                    id=utils.normalizeString(ki),
                    title=vi
                )
                subtopic = topic[sid]
                subtopic.setAcquireCriteria(True)
                c = subtopic.addCriterion(
                    'getTimePeriods', 'ATSimpleStringCriterion')
                c.setValue(ki)
                topic.setSortCriterion('sortable_title', reversed=False)

        return 1
