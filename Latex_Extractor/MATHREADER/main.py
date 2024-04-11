import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

mathreader_dir = os.path.join(current_dir,'..','..','Libs','mathreader')

sys.path.append(mathreader_dir)

import mathreader
import mathreader.api
import mathreader.config as Configuration