from json import loads
from os.path import join, dirname
import setuptools


def read(filename):
    path = join(dirname(__file__), filename)
    with open(path, 'rt') as file:
        return file.read()


package = loads(read('package.json'))

setuptools.setup(name='hmlr-design-system',
                 version=package['version'],
                 description='HMLR Design System',
                 packages=['hmlr_design_system'],
                 package_dir={'': 'src'},
                 package_data={'hmlr_design_system': ['**/template.html']}
                 )
