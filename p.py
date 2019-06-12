import os
import sys
import inspect

PATH__ = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, PATH__)
