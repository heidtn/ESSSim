from setuptools import setup

setup(
    name='ESSSim',
    version='0.1.0',
    author='Nathaniel Heidt',
    author_email='NathanielHeidt@gmail.com',
    packages=['ESSSim'],
    license='LICENSE.txt',
    description='Simulation framework for the EVO space suit',
    long_description=open('README.md').read(),
    install_requires=['numpy', 'clive-log'],
)
