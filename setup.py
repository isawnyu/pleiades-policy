from setuptools import setup, find_packages

version = '0.2'

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
      author_email='sgillies@frii.com',
      url='http://atlantides.org/trac/pleiades/wiki/PleiadesPolicy',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pleiades'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools', 
          'pleiades.workspace',
          'pleiades.vocabularies',
          'pleiades.atom',
          'pleiades.json',
          'pleiades.kml',
          'pleiades.openlayers'      
          ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
