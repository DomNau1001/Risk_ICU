from setuptools import setup, find_packages

setup(
    name='risk_icu',
    version='1.0',
    description='A package for ICU risk assessment',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'pandas',
        'scipy'
    ]
)
