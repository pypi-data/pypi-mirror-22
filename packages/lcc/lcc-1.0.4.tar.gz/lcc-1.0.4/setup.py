
# from distutils.core import setup
import pkgutil

import os
from setuptools import setup, find_packages


def getPackages(path="."):
    p = list()
    for importer, modname, ispkg in pkgutil.walk_packages(path=path, onerror=lambda x: None):
	if "." in modname:
	    p.append( modname[:modname.rfind(".")] )
    p.append("lcc.gavo.votable")
    p.append("lcc.gavo.utils")
    p.append("lcc.gavo.stc")
    return p

setup(
  name = 'lcc',
  packages = find_packages(),
  version = '1.0.4',
  description = 'Light Curves Classifier is package for classification stars by using their light curves and metadata',
  author = 'Martin Vo',
  author_email = 'mavrix@seznam.cz',
  url = 'https://github.com/mavrix93/LightCurvesClassifier', 
  download_url = 'https://github.com/mavrix93/LightCurvesClassifier/archive/0.1.tar.gz', 
  install_requires = ["numpy", "scipy", "matplotlib", "pandas", "PyBrain", "pyfits", "scikit-learn", "kplr", "astroML", "astropy", "requests", "bs4", "pathos"],
  keywords = ['light curves', 'classifying', 'machine-learning', 'astronomy', 'data-mining'],
  classifiers = [],
)

