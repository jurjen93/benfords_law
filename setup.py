from setuptools import setup

setup(
   name="benford_analysis",
   version='0.0.1',
   author='Jurjen de Jong',
   author_email='jurjendejong93@gmail.com',
   packages=[],
   scripts=[],
   url='https://github.com/jurjen93/Benfords_law',
   license='LICENSE.txt',
   description="Use this package to analyse your data with Benford's law",
   long_description=open('README.md').read(),
   install_requires=[
       "matplotlib",
       "scipy",
   ],
)