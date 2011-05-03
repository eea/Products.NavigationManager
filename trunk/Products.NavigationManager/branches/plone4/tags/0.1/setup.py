""" setup.py """

from setuptools import setup, find_packages
import os

name = 'Products.NavigationManager'
path = name.split('.') + ['version.txt']
version = open(os.path.join(*path)).read().strip()

setup(
 name='Products.NavigationManager',
 version=version,
 description="NavigationManager skin for EEA",
 long_description=open("README.txt").read() + "\n" +
                  open(os.path.join("docs", "HISTORY.txt")).read(),
 url="https://svn.eionet.europa.eu/projects/"
     "Zope/browser/trunk/Products.NavigationManager",
 classifiers=[
   "Framework :: Plone",
   "Programming Language :: Python",
   ],
 keywords='EEA Products NavigationManager',
 author='Antonio de Marinis (EEA), European Environment Agency',
 author_email='webadmin@eea.europa.eu',
 license='GPL',
 packages=find_packages(exclude=['ez_setup']),
 namespace_packages=['Products'],
 include_package_data=True,
 zip_safe=False,
 install_requires=[
     "setuptools",
 ],
 entry_points="""
 # -*- Entry points: -*-
 """,
 )

