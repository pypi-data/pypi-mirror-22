# Copyright 2015, John Kitchin
# (see accompanying license files for details).

from distutils.core import setup

setup(name='pycse',
      version='1.6.4',
      description='python computations in science and engineering',
      url='http://github.com/jkitchin/pycse',
      maintainer='John Kitchin',
      maintainer_email='jkitchin@andrew.cmu.edu',
      license='GPL',
      platforms=['linux'],
      packages=['pycse'],
      scripts=['pycse/publish.py'],
      install_requires=['quantities==0.10.1'],
      data_files=['requirements.txt', 'LICENSE'],
      long_description='''\
python computations in science and engineering
===============================================

This package provides some utilities to perform:
1. linear and nonlinear regression with confidence intervals
2. Solve some boundary value problems.

See http://kitchingroup.cheme.cmu.edu/pycse for documentation.

      ''')

# python setup.py register to setup user
# to push to pypi - (shell-command "python setup.py sdist upload")
