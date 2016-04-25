from zope.interface import implements
from zope.interface import Interface

from zope.component import adapts
from plone.app.caching.interfaces import IETagValue


class Accept(object):
    """The ``accept`` etag component, returning the value of the
    HTTP_ACCEPT request key.
    """

    implements(IETagValue)
    adapts(Interface, Interface)

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def __call__(self):
        """Normalize Accept header"""
        return ','.join(set(s.strip() for s in
                            self.request.get('HTTP_ACCEPT', '').split(',')))
