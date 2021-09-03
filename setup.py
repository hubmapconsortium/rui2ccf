from distutils.core import setup

from setuptools import find_packages

from rui2ccf import __version__

classifiers = """
Development Status :: 4 - Beta
Environment :: Console
License :: OSI Approved :: GNU General Public License (GPL)
Intended Audience :: Science/Research
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Bio-Informatics
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Operating System :: POSIX :: Linux
""".strip().split('\n')

setup(name='rui2ccf',
      version=__version__,
      description='A Python tool to convert RUI objects to CCF Spatial Ontology (CCF-SO)',
      author='Josef Hardi',
      author_email='johardi@stanford.edu',
      url='https://github.com/metadatacenter/rui2ccf',
      license='GPL-3.0',
      classifiers=classifiers,
      install_requires=[
          'rdflib==5.0.0',
          'stringcase==1.2.0',
          'requests_file==1.5.1'
      ],
      python_requires='>=3.5, <3.9',
      test_suite='nose.collector',
      tests_require=['nose'],
      packages=find_packages(),
      include_package_data=True,
      scripts=['bin/rui2ccf'])
