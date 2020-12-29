from setuptools import setup, find_packages

with open('requirements.txt') as f:
    reqs = f.read()

setup(
    name='coding',
    version='0.1',
    packages=find_packages(include=["redbaron_type_hinting"]),
    # license='LICENSE.txt',
    long_description=open('README.md').read(),
    install_requires=reqs.strip().split('\n'),
)