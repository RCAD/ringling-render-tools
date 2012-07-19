from setuptools import setup, find_packages
from pkg_resources import Requirement, resource_filename
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'src')))
import rrt
setup(
    name = "ringling_render_tools",
    version = rrt.__version__,
    author = "Owen Nelson, Stephen Garcia",
    author_email = "onelson@ringling.edu, sgmorale@ringling.edu",
    license = "MIT",
    description = "Pipeline tools for Maya, 3DSmax, and C4D rendering with Windows HPC",
    keywords = "Maya 3DSmax C4D WindowsHPC",
    platforms = ["windows"],
    package_dir = {'':'src'},
    packages = find_packages('src'),
    include_package_data = True,
    install_requires = ['setuptools'],
    extras_require = {'pymel': ['pymel>=1']},
    dependency_links = ['http://pymel.googlecode.com/files/pymel-1.0.2.zip'],
    test_suite = 'nose.collector',
    tests_require = ['nose','ludibrio','pymel'],
    entry_points = {
        'console_scripts': [
            'hpc-node-prep = rrt.hpc.scripts:prep_delegator',
            'hpc-node-release = rrt.hpc.scripts:release_delegator',
            'hpc-deploy-extras = rrt.hpc.scripts:deploy_extras',
        ],
        'gui_scripts': [
            'hpc-submit-max = rrt.max.gui:submit_gui',
            'hpc-submit-md = rrt.md.gui:submit_gui',
            'hpc-submit-maya = rrt.maya.outsideGui:submit_gui',
        ]
    }
)
