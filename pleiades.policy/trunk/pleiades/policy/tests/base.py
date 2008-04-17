from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

ztc.installProduct('ATVocabularyManager')
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
    
    ztc.installProduct('pleiades.policy')
    ztc.installProduct('pleiades.vocabulary')
    
# The order here is important: We first call the (deferred) function which
# installs the products we need for the Pleiades package. Then, we let 
# PloneTestCase set up this product on installation.

setup_pleiades_policy()
ptc.setupPloneSite(products=['ATVocabularyManager', 'PleiadesEntity', 'pleiades.policy'])

class PleiadesPolicyTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """
