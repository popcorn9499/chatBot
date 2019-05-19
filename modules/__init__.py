import os
import importlib

__globals = globals()

for file in os.listdir(os.path.dirname(__file__)):
    if file.find(".py") != -1:
        mod_name = file[:-3]   # strip .py at the end
        __globals[mod_name] = importlib.import_module('.' + mod_name, package=__name__.replace(".__init__", ""))