from setuptools import setup, find_packages
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'src')))
import ringling
setup(
    name = "ringling_render_tools",
    version = ringling.__version__,
    package_dir = {'':'src'},
    packages = find_packages('src'),

    install_requires = ['pymel'],
#    dependency_links = ['http://code.google.com/p/pymel/'],
    dependency_links = ['http://pymel.googlecode.com/files/pymel-1.0.2.zip'],
    author = "Owen Nelson",
    author_email = "onelson@ringling.edu",
    description = "Pipeline tools for Maya and 3DSmax rendering with Windows HPC",
    keywords = "Maya 3DSmax WindowsHPC",
    zip_safe = False,
    
    entry_points = {
        'console_scripts': [
            'hpc-node-prep = ringling.hpc.scripts:prep_delegator',
            'hpc-node-release = ringling.hpc.scripts:release_delegator',
        ],
        'gui_scripts': []
    }

)
