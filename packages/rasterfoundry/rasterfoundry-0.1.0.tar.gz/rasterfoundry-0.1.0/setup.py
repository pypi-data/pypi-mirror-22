import setuptools

setuptools.setup(
    name="rasterfoundry",
    version="0.1.0",
    description='A Python client for Raster Foundry, a web platform for '
    'combining, analyzing, and publishing raster data.',
    long_description=open('README.rst').read(),
    url='https://github.com/azavea/raster-foundry-python-client',
    author='Raster Foundry',
    author_email='info@rasterfoundry.com',
    license='Apache License 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='raster earth-observation geospatial geospatial-processing',
    packages=setuptools.find_packages(exclude=['tests']),
    package_data={'': ['*.yml']},
    install_requires=[
        'cryptography >= 1.3.2',
        'pyasn1 >= 0.2.3',
        'requests >= 2.9.1',
        'bravado >= 8.4.0'
    ],
    extras_require={
        'dev': [],
        'test': [],
    },
    tests_require=[],
)
