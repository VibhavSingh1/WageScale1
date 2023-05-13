from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name="WageScale",
    version='0.0.1',
    description='Web-Application providing salary and job related utils',
    long_description=readme,
    author='Vibhav Singh',
    author_email='vibhav.singh0v@gmail.com',
    license=license,
    packages=find_packages(exclude=('docs')),
    include_package_data=True,
)
