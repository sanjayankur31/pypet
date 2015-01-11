"""Module running all examples in the examples directory

Suppresses all openings of plots
"""
__author__ = 'Robert Meyer'

import matplotlib
matplotlib.use('Agg')

import glob
import os
import sys
try:
    import brian
except ImportError:
    print('No BRIAN module found, will skip the example')
    brian = None


os.chdir(os.path.join('..','..','examples'))
sys.path.append(os.getcwd())
simple_examples = glob.glob('*.py')

assert len(simple_examples) == 11 + 1

for simple_example in simple_examples:
    if simple_example == '__init__':
        continue

    filename = os.path.join(os.getcwd(), simple_example)
    if 'brian' in simple_example and brian is None:
        print("---------- Skipping %s ----------" % simple_example)
    else:
        print("########## Running %s ###########" % simple_example)
        #execfile(filename, globals(), locals())
        with open(filename) as f:
            code = compile(f.read(), filename, 'exec')
            exec(code, globals(), locals())


ex13 = 'example_13_post_processing'
print("########## Running %s ###########" % ex13)
os.chdir(ex13)
sys.path.append(os.getcwd())
print("Running main")
filename = os.path.join(os.getcwd(), 'main.py')
with open(filename) as f:
    code = compile(f.read(), filename, 'exec')
    exec(code, globals(), locals())
print("Running analysis")
filename = os.path.join(os.getcwd(), 'analysis.py')
with open(filename) as f:
    code = compile(f.read(), filename, 'exec')
    exec(code, globals(), locals())
print("Running pipeline")
filename = os.path.join(os.getcwd(), 'pipeline.py')
with open(filename) as f:
    code = compile(f.read(), filename, 'exec')
    exec(code, globals(), locals())

if brian is not None:
    ex11 = 'example_11_large_scale_brian_simulation'
    print("########## Running %s ###########" % ex11)
    os.chdir('..')
    os.chdir(ex11)
    sys.path.append(os.getcwd())
    print("Running script")
    filename = os.path.join(os.getcwd(), 'runscript.py')
    with open(filename) as f:
        code = compile(f.read(), filename, 'exec')
        exec(code, globals(), locals())
    print("Running analysis")
    filename = os.path.join(os.getcwd(), 'plotff.py')
    with open(filename) as f:
        code = compile(f.read(), filename, 'exec')
        exec(code, globals(), locals())