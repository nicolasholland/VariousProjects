from setuptools import find_packages, setup

setup(
    name='merrychristmas',
    description='Tensorflow style transfer for the family',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'tensorflow',
    ],
)
