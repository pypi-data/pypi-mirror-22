#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Ce module est un test de client parapheur
"""
__version__ = "0.3.1-6266"


def getrestclient():
    # We have to define it here, because we use it everywhere in scripts
    import parapheur
    return parapheur.getrestclient()


def getsoapclient(user=None, password=None):
    import parapheur
    return parapheur.getsoapclient(user, password)