import os
import sys
import inspect

PATH__ = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
print(PATH__)
#sys.path.insert(0, PATH__)