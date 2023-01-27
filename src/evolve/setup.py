from setuptools import setup, find_packages
from pathlib import Path

# with open("README.md","r") as fh:
#     long_description = fh.read()

# Net lOad wiTh DERs
setup(
    name='evolve',
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    version='2.0',
    description='Net load evolution with DERs',
    author='Kapil Duwadi',
    author_email='kapil.duwadi@nrel.gov',
    packages=find_packages(Path(__file__).parents[0] / 'src'),
    url="https://github.com/NREL/evolve",
    keywords="Energy Storage, PV, Electric Vehicle, Net load, Distribution System",
    package_dir={"": "src"},   
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent"
    ]
)