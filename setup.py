from setuptools import find_packages, setup

setup(
    name='PyDashie',
    version='0.1dev',
    packages=[
        'pydashie',
    ],
    install_requires=['Flask >= 0.10', 'Coffeescript >= 1.0.8', 'pyScss >= 1.2.0'],
    entry_points={'console_scripts': ['pydashie = pydashie.__main__:run_app']},
    license='MIT',
    long_description=open('README.rst').read(), )
