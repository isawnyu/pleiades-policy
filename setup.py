from setuptools import setup, find_packages

version = '0.3.1'

setup(name='pleiades.policy',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Sean Gillies',
      author_email='sean.gillies@gmail.com',
      url='http://atlantides.org/trac/pleiades/wiki/PleiadesPolicy',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pleiades'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'pleiades.workspace',
          'pleiades.vocabularies',
          'pleiades.geographer',
          'pleiades.atom',
          'pleiades.iterate',
          'pleiades.json',
          'pleiades.kml',
          'pleiades.openlayers',
          'pleiades.portlet.references',
          'pleiades.notredame',
          'pleiades.sitemap',
          'pleiades.placematch',
          'pleiades.vaytrouindex',
          'pleiades.neighbors',
          'archetypes.referencebrowserwidget',
          'pleiades.reconciliation',
          'Products.PleiadesEntity',
          ],
      extras_require={
          'test': ['Products.PloneTestCase'],
      },
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
