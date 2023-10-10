from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as file_pointer:
    long_description = file_pointer.read()

with open("requirements.txt", "r", encoding="utf-8") as file_pointer:
    requirements = file_pointer.read().splitlines()

setup(
    name="evolve-core",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="1.0.0",
    description="Modern tool for understanding impact of distributed energy resources on net load.",
    author="Kapil Duwadi",
    author_email="kapil.duwadi@nrel.gov",
    packages=find_packages(),
    url="https://github.com/NREL/evolve",
    keywords="Energy Storage, PV, Electric Vehicle, Net load, Distribution System",
    python_requires=">=3.10",
    install_requires=requirements,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)
