from setuptools import setup, find_packages

with open("README.md","r") as fh:
    long_description = fh.read()

# Net lOad wiTh DERs
setup(
    name='NOTE',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='v1.4-alpha',
    description='Net load evolution with DERs',
    author='Kapil Duwadi',
    author_email='kapil.duwadi@nrel.gov',
    packages=find_packages("EMeRGE"),
    url="https://github.com/NREL/NOTE",
    keywords="Energy Storage, PV, Electric Vehicle, Net load, Distribution System",
    install_requires=["statsmodels==0.10.0",
                        "pandas==0.24.2",
                        "seaborn==0.9.0",
                        "matplotlib==3.1.0",
                        "numpy==1.16.4"],
    package_dir={"": "src"},   
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent"
    ]
)