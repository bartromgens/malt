#! /usr/bin/python

import shutil
import os

from datetime import datetime

now = datetime.now()
nowStr = now.strftime('%Y%m%d')
shutil.copy('../malt.sqlite', '../backup/' + nowStr + 'malt.sqlite')