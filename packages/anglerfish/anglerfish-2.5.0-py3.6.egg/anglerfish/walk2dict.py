#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Convert bytes to kilobytes, megabytes, gigabytes, etc."""


import os

from collections import OrderedDict
from json import dumps


def walk2dict(folder, links=False, showhidden=False,
              strip=False, jsony=False, ordereddict=False):
    """Return Nested Dictionary represents folder/file structure of folder."""
    ret = []
    for path, dirs, files in os.walk(folder, followlinks=links):
        if not showhidden:
            dirs = [_ for _ in dirs if not _.startswith(".")]
            files = [_ for _ in files if not _.startswith(".")]
        a = {}
        if strip:
            p = path.strip(folder + os.sep)
        else:
            p = path
        if len(p.split(os.sep)) == 1:
            parent = ''
        if len(p.split(os.sep)) > 1:
            parent = os.sep.join(p.split(os.sep)[:-1])
        if path == folder:
            parent = 'root'
        a['path'] = p
        a['fullpath'] = os.path.abspath(path)
        a['parent'] = parent
        a['dirs'] = dirs
        a['files'] = []
        for fyle in files:
            try:  # sometimes os.stat(ff) just fails,breaking all the loop.
                f = {}
                ff = path + os.sep + fyle
                (mode, ino, dev, nlink, uid, gid, size,
                 atime, mtime, ctime) = os.stat(ff)
                f['name'] = fyle
                f['mode'] = mode
                f['ino'] = ino
                f['dev'] = dev
                f['nlink'] = nlink
                f['uid'] = uid
                f['gid'] = gid
                f['size'] = size
                f['atime'] = atime
                f['mtime'] = mtime
                f['ctime'] = ctime
                a['files'].append(f)
            except Exception:
                pass
        ret.append(a)
    dict_of_files = ret[0]
    if ordereddict:  # dictionary sorted by key.
        dict_of_files = OrderedDict(sorted(ret[0].items(), key=lambda t: t[0]))
    if jsony:  # json
        dict_of_files = dumps(dict(dict_of_files), sort_keys=True, indent=4)
    return dict_of_files
