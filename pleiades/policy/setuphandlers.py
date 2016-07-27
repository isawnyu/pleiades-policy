from Acquisition import aq_base
import logging
import transaction
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.log import log

COMMIT_LIMIT = 50


def install_caching(context):
    qi = getToolByName(context, 'portal_quickinstaller')
    if not qi.isProductInstalled('plone.app.caching'):
        qi.installProduct('plone.app.caching')
        portal_setup = getToolByName(context, 'portal_setup')
        portal_setup.runAllImportStepsFromProfile(
            'profile-plone.app.caching:with-caching-proxy', purge_old=False)
        portal_setup.runImportStepFromProfile(
            'profile-pleiades.policy:default', 'plone.app.registry',
            run_dependencies=False, purge_old=False)


def update_rolemap(context):
    if getattr(context, 'getSite', None) is not None:
        site = context.getSite()
        if context.readDataFile("pleiades.policy_various.txt") is None:
            return
    else:
        site = context
    p_jar = site._p_jar
    log('Updating workflow mapping for %s' % site.absolute_url(1),
        severity=logging.WARNING)
    wft = getToolByName(site, 'portal_workflow')
    wfs = {}
    for id in wft.objectIds():
        wf = wft.getWorkflowById(id)
        if hasattr(aq_base(wf), 'updateRoleMappingsFor'):
            wfs[id] = wf

    def update_mappings(ob, count, last_count):
        wf_ids = wft.getChainFor(ob)
        if wf_ids:
            changed = 0
            for wf_id in wf_ids:
                wf = wfs.get(wf_id, None)
                if wf is not None:
                    did = wf.updateRoleMappingsFor(ob)
                    if did:
                        changed = 1
            if changed:
                count = count + 1
                if count % COMMIT_LIMIT == 0:
                    transaction.savepoint(optimistic=True)
                    log('Savepoint after updating %d items' % count,
                        severity=logging.WARNING)
                    p_jar.cacheMinimize()

        if hasattr(aq_base(ob), 'objectItems'):
            obs = ob.objectItems()
            if obs:
                for k, v in obs:
                    changed = getattr(v, '_p_changed', 0)
                    count, last_count = update_mappings(v, count, last_count)
                    if changed is None:
                        # Re-ghostify.
                        v._p_deactivate()
                    if count - last_count >= COMMIT_LIMIT:
                        transaction.commit()
                        last_count = count
                        log('Commit after updating %d items' % count,
                            severity=logging.WARNING)

                    p_jar.cacheMinimize()

        return count, last_count

    count, last_count = update_mappings(site, 0, 0)
    log('Updated %d items' % count, severity=logging.WARNING)
    return
