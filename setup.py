import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='stig_parser',  
    version='1.0.1',
    author="Peter Keech",
    author_email="peter.a.keech@gmail.com",
    description="A Python module to parse DISA STIG (XCCDF) Files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pkeech/stig_parser",
    packages=setuptools.find_packages(),
    install_requires=[
        'xmltodict'
    ],
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)