from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Testing import ZopeTestCase as ztc

ztc.installProduct('Products.CompoundField')
ztc.installProduct('Products.ATBackRef')
ztc.installProduct('PleiadesEntity')


@onsetup
def setup_pleiades_policy():
    """Set up the additional products required for the Pleiades site policy.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """

    fiveconfigure.debug_mode = True
    import pleiades.policy
    zcml.load_config('configure.zcml', pleiades.policy)
    fiveconfigure.debug_mode = False

    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML.
    ztc.installPackage('pleiades.vocabularies')
    ztc.installPackage('pleiades.workspace')
    ztc.installPackage('pleiades.geographer')
    ztc.installPackage('pleiades.policy')
    ztc.installPackage('pleiades.kml')


# The order here is important: We first call the (deferred) function which
# installs the products we need for the Pleiades package. Then, we let
# PloneTestCase set up this product on installation.
setup_pleiades_policy()
ptc.setupPloneSite(
    products=[
        'Products.CompoundField', 'Products.ATBackRef',
        'PleiadesEntity', 'pleiades.policy'
    ],
)


class PleiadesPolicyTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """


class PleiadesPolicyWorkflowTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """

    def afterSetUp(self):
        self.catalog = self.portal.portal_catalog
        self.workflow = self.portal.portal_workflow
        self.workflow.setChainForPortalTypes(
            ['Place', 'PlaceContainer', 'Name'], 'pleiades_entity_workflow')

        self.portal.acl_users._doAddUser('member', 'secret', ['Member'], [])
        self.portal.acl_users._doAddUser('manager', 'secret', ['Manager'], [])
        self.portal.acl_users._doAddUser('editor', ' secret', ['Editor'], [])
        self.portal.acl_users._doAddUser('reviewer', 'secret', ['Reviewer'], [])
        self.portal.acl_users._doAddUser('reader', 'secret', ['Reader'], [])
        self.portal.acl_users._doAddUser(
            'contributor', 'secret', ['Contributor'], [])
