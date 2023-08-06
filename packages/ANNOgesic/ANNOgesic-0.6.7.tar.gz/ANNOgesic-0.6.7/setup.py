try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='ANNOgesic',
    version='0.6.7',
    packages=['annogesiclib'],
    author='Sung-Huan Yu',
    author_email='sung-huan.yu@uni-wuerzburg.de',
    description='ANNOgesic - The pipeline for bacterial/archaeal RNA-Seq based genome annotations',
    url='',
    install_requires=[
        "biopython >= 1.65",
        "matplotlib >= 1.5.0",
        "numpy >= 1.9.2",
        "networkx >= 1.9.1"
    ],
    scripts=['bin/annogesic'],
    license='ISC License (ISCL)',
    classifiers=[
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ]
)
