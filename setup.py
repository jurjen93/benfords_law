from setuptools import setup, find_packages

with open('README.md') as f:
   long_description = f.read()

setup(
   name="benfordslaw_analysis",
   version='1.1.0',
   author='Jurjen de Jong',
   author_email='jurjendejong93@gmail.com',
   url='https://github.com/jurjen93/Benfords_law',
   license='LICENSE.txt',
   description="Use this package to analyse your data with Benford's law",
   long_description=long_description,
   long_description_content_type="text/markdown",
   install_requires=[
       "matplotlib",
       "scipy",
      "pandas"
      ],
   packages=find_packages()
   )