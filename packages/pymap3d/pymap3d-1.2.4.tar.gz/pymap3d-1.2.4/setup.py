#!/usr/bin/env python
req = ['python-dateutil','pytz','nose','numpy','astropy']
# %%
import pip
try:
    import conda.cli
    conda.cli.main('install',*req)
except Exception as e: 
    pip.main(['install'] + req)
# %%
from setuptools import setup

setup(name='pymap3d',
      packages=['pymap3d'],
      version = '1.2.4',
      description='Python coordinate conversions, following convention of several popular Matlab routines.',
      author = 'Michael Hirsch, Ph.D.',
      url = 'https://github.com/scivision/pymap3d',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 5 - Production/Stable',
      'License :: OSI Approved :: BSD License',
      'Topic :: Scientific/Engineering :: GIS',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python',
      ],
      install_requires=req,
	  )

