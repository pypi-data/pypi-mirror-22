import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
	name='python-boltz',
	version='0.0.1',
	packages=find_packages(),
	include_package_data=True,
	license='MIT License',  # example license
	description='API for authenticating modem users with bolt account.',
	long_description=README,
	url='',
	install_requires=[
		  'beautifulsoup4',
		  'requests'],
	author='Yanwar Solahudin',
	author_email='yanwarsolah@gmail.com',
	classifiers=[
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Topic :: Internet :: WWW/HTTP',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	],
)
