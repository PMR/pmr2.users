from Zope2.App import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase.layer import onsetup, onteardown
from Products.PloneTestCase import PloneTestCase as ptc

@onsetup
def setup():
    import pmr2.users
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', pmr2.users)
    fiveconfigure.debug_mode = False

@onteardown
def teardown():
    pass

setup()
teardown()
