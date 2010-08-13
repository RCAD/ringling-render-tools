from setuptools import setup, find_packages
from pkg_resources import Requirement, resource_filename
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'src')))
import rrt
setup(
    name = "ringling_render_tools",
    version = rrt.__version__,
    author = "Owen Nelson",
    author_email = "onelson@ringling.edu",
    license = "MIT",
    description = "Pipeline tools for Maya and 3DSmax rendering with Windows HPC",
    keywords = "Maya 3DSmax WindowsHPC",
    package_dir = {'':'src'},
    packages = find_packages('src'),
    extras_require = {'pymel': ['pymel>=1']},
    tests_require = ['nose'],
    dependency_links = ['http://pymel.googlecode.com/files/pymel-1.0.2.zip'],
    test_suite = 'nose.collector',
    include_package_data = True,
    entry_points = {
        'console_scripts': [
            'hpc-node-prep = rrt.hpc.scripts:prep_delegator',
            'hpc-node-release = rrt.hpc.scripts:release_delegator',
            'hpc-deploy-extras = rrt.hpc.scripts:deploy_extras'
        ],
        'gui_scripts': []
    }
)
