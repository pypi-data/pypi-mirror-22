from setuptools import setup
from fact import __version__


setup(
    name='pyfact',
    version=__version__,
    description='A module containing useful methods for working with fact',
    url='http://github.com/fact-project/pyfact',
    author='Maximilian Noethe, Dominik Neise',
    author_email='maximilian.noethe@tu-dortmund.de',
    license='MIT',
    packages=[
        'fact',
        'fact.plotting',
        'fact.slowdata',
        'fact.credentials',
        'fact.auxservices',
        'fact.factdb',
        'fact.analysis',
    ],
    package_data={
        '': ['resources/*', 'credentials/credentials.encrypted']
    },
    tests_require=['pytest>=3.0.0'],
    setup_requires=['pytest-runner'],
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib>=1.4',
        'python-dateutil',
        'pymongo>=2.7',
        'simple-crypt',
        'setuptools',
        'sqlalchemy',
        'pymysql',
        'pandas',
        'astropy',
        'peewee',
        'h5py',
        'wrapt',
        'tables',  # pytables in anaconda
    ],
    zip_safe=False,
)
