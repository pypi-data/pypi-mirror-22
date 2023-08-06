#!/usr/bin/env python

from distutils.core import setup
import atproject

setup(
    name="atproject",
    version=1.1,
    author="Chris Markiewicz, Bram Cohen, John Hoffman, Uoti Arpala et. al., AT_group",
    author_email="<liuyifei0226@gmail.com>",
    url="https://github.com/atproject/",
    description="John Hoffman's fork of the original bittorrent, for Academictorrents.com. We made some modifications and created API to download files listed at Academictorrents.com",
    license="MIT",
    py_modules=['academictorrents'],
    package_data={'atproject':['atproject/icons/*.ico']},
    include_package_data=True,
    packages=["atproject",
    		  "atproject.Application",
              "atproject.Client",
              "atproject.Meta",
              "atproject.Network",
              "atproject.Storage",
              "atproject.Tracker",
              "atproject.Download"
             ],
    install_requires=[
          'win_inet_pton',
      ],
    scripts=["academictorrents.py"]
)
