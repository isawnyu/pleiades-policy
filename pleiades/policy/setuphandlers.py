from Products.CMFCore.utils import getToolByName


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
