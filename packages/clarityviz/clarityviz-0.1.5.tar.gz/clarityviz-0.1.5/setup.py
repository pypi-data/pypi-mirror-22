#!/usr/bin/env python

# read online that setuptools is preferred to distutils
from setuptools import setup, find_packages

import clarityviz

VERSION = clarityviz.version

setup(
    name='clarityviz',
    packages=find_packages(exclude=['docs', 'tests*']),
    #scripts = [],
    entry_points = {
#        'console_scripts': [
#            'clarityviz=clarityviz:main',
#        ],    
    },
    version=VERSION,
    description='A pipeline used to vizualize and analyze clarity treated brain images.',
    author='Albert Lee, Jonathan Liu, Tony Sun, Luke Zhu',
    author_email='albertlee@jhu.edu, jliu118@jhu.edu, tsun11@jhu.edu, lzhu20@jhu.edu',
    url='https://github.com/NeuroDataDesign/seelviz',
    download_url='https://github.com/alee156/clviz/tarball/0.1.5',
    keywords=[
        'clarity',
        'brain',
        'histogram equalization',
        'connectivity',
        'plotly'
    ],
    license='',
    data_files=None,
    classifiers=[
        'Development Status :: 3 - Alpha',
        #'Intended Audience :: Researchers',
        #'License :: ::',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4'
    ],
    install_requires=[]
)
