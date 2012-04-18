import sys
import imp

class Module_Creator(object):
    count = 0
    
    def __init__(self, name, code):
        self.module = imp.new_module('custom_module_' + str(Module_Creator.count))
        Module_Creator.count += 1
        self.blank_module_dict = self.module.__dict__.copy()
        exec code in my_module.__dict__

    def remove_module(self):
        for k,v in my_module.__dict__.items():
            if blank_module_dict.has_key(k):
                my_module.__dict__.pop(k)
