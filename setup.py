from setuptools import setup, find_packages


setup(
    name='cases',
    version='0.1',
    author='Javier Santacruz',
    author_email='javier.santacruz@avature.net',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
)
