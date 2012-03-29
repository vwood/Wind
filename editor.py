#!/usr/bin/env python

import sys
import imp

my_code = 'a = 5'

# Do we really need to name this?
my_module = imp.new_module('my_module')
blank_module_dict = my_module.__dict__.copy()

exec my_code in my_module.__dict__

print my_module.a

for k,v in my_module.__dict__.items():
    if blank_module_dict.has_key(k):
        my_module.__dict__.pop(k)

exec my_code in my_module.__dict__

print my_module.a

## to prevent re-importing
# sys.modules['my_module'] = my_module
