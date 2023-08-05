# -*- coding: utf-8 -*-
import sys, os
from setuptools import setup

__version__='0.7.10'

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist bdist_egg register upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (__version__,__version__))
    print("  git push --tags")
    sys.exit()

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='gseapy',
      version=__version__,
      description='Gene Set Enrichment Analysis in Python',
      long_description=readme(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 2.7',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Software Development :: Libraries'],
      keywords= ['GO', 'Gene Ontology', 'Biology', 'Enrichment',
          'Bioinformatics', 'Computational Biology',],
      url='https://github.com/BioNinja/gseapy',
      author='Zhuoqing Fang',
      author_email='fangzhuoqing@sibs.ac.cn',
      license='MIT',
      packages=['gseapy'],     
      install_requires=[
          'numpy>=1.8.0',
          'pandas>=0.16',
          'matplotlib>=1.4.3',
          'beautifulsoup4>=4.4.1',
          'requests',
          'lxml',
          'html5lib',],
      entry_points={'console_scripts': ['gseapy = gseapy.__main__:main'],},
      
      zip_safe=False,
      download_url='https://github.com/BioNinja/gseapy',)
      
__author__ = 'Zhuoqing Fang'
