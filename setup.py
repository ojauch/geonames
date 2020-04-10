import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='geonames-ojauch',
    version='0.0.1',
    author='Oskar Jauch',
    author_email='oskar.jauch@posteo.de',
    description='Library for geonames API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ojauch/geonames',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6'
)
