from setuptools import setup, find_packages

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(
    name='risk_icu',
    version='1.0',
    description='A package for ICU risk assessment',
    packages=find_packages(),
    install_requires=requirements,
)
