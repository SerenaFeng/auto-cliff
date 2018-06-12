import os

this_dir = os.path.dirname(os.path.realpath(__file__))
print this_dir
templates_dir = os.path.join(this_dir, 'cliff_generator/templates/')

print templates_dir

pdir = '/Users/serena/github/test_dir'

for root, dirs, files in os.walk(templates_dir):
    relative_dir = root.replace(templates_dir, '')
    print relative_dir
    print root, dirs, files
