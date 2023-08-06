
from setuptools import setup

setup(
    name='PLAMS',
    version='1.1.1',
    author='Michał Handzlik',
    author_email='handzlik@scm.com',
    url='https://www.scm.com/doc/plams/',
    download_url='https://github.com/SCM-NV/PLAMS/zipball/release',
    license='LGPLv3',
    description='Python Library for Automating Molecular Simulations',
    long_description="PLAMS is a library providing powerful, flexible and easily extendable Python interface to molecular modeling programs. It takes care of input preparation, job execution, file management and output data extraction. It helps with building advanced data workflows that can be executed in parallel, either locally or by submitting to a resource manager queue.\n\nPlease check the project's GitHub page for more information: https://github.com/SCM-NV/PLAMS \n\nPLAMS is an Open Source project supported by `Scientific Computing & Modelling NV (SCM) <https://www.scm.com>`_",
    classifiers=[
            'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
            'Development Status :: 4 - Beta',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.5',
            'Topic :: Scientific/Engineering :: Chemistry',
            'Topic :: Scientific/Engineering :: Physics',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['molecular modeling', 'computational chemistry', 'workflow', 'python interface'],
    install_requires=[
        'dill>=0.2.4',
        'numpy',
        'six',
    ],
    package_dir={'': 'src'},
    packages=['scm.plams', 'scm.plams.core', 'scm.plams.tools', 'scm.plams.interfaces', 'scm'],
    package_data={'scm.plams':['plams_defaults']},
    namespace_packages = ['scm'],
    scripts=['bin/plams']
)
