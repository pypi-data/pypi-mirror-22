from distutils.core import setup
from setuptools import find_packages

INSTALL_REQUIREMENTS = [
    'Django>=1.10.5',
    'django-cms>=3.4.2',
    'pcart-core>=1.98.4',
    'pcart-catalog>=1.98.8',
    'pcart-customers>=1.98.5',
]

setup(
    name='pcart-statistics',
    version='1.98.2',
    author='Oleh Korkh',
    author_email='oleh.korkh@the7bits.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    license='BSD License',
    description='A powerful e-commerce solution for Django CMS',
    long_description=open('README.txt').read(),
    platforms=['OS Independent'],
    url='http://the7bits.com/',
    install_requires=INSTALL_REQUIREMENTS,
)
