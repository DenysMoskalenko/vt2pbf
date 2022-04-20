from setuptools import find_packages, setup

packages = (
    'vt2pbf',
    'vt2pbf.mapbox',
    'vt2pbf.service',
)
requires = (
    'protobuf>=3.6.0,<4',
)

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vt2pbf',
    version='0.1.1',
    description='Python library for encoding mapbox vector tiles into tile_pbf',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='DenysMoskalenko',
    license='MIT',
    url='https://github.com/DenysMoskalenko/vt2pbf',
    packages=find_packages(include=packages),
    install_requires=requires,
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=7.1.1<8'],
    test_suite='tests',
)
