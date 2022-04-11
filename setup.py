from setuptools import find_packages, setup

packages = (
    'vt2pbf',
    'vt2pbf.mapbox',
    'vt2pbf.service',
)
requires = (
    'protobuf>=3.20.0,<4',
)

setup(
    name='vt2pbf',
    packages=find_packages(include=packages),
    version='0.0.2',
    description='Python library for encoding mapbox vector tiles into pbf',
    author='DenysMoskalenko',
    license='MIT',
    install_requires=requires,
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=7.1.1<8'],
    test_suite='tests',
)
