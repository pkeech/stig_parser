## IMPORT REQUIRED DOCUMENTS
import setuptools, subprocess, os

## PARSE README TO LONG DESCRIPTION
with open("README.md", "r") as fh:
    long_description = fh.read()

## QUERY GITHUB FOR TAG TO GENERATE VERSION
new_version = (
    subprocess.run(["git", "describe", "--tags"], cwd="/home/runner/work/stig_parser/stig_parser", stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

## DEFINE PACKAGE VERSION
assert "." in new_version
assert os.path.isfile("src/stig_parser/version.py")
with open("src/stig_parser/VERSION", "w", encoding="utf-8") as fh:
    fh.write(f"{new_version}\n")

## DEFINE PACKAGE
setuptools.setup(
    name='stig_parser',  
    version=new_version,
    license='MIT',
    author="Peter Keech",
    author_email="peter.a.keech@gmail.com",
    description="A Python module to parse DISA STIG (XCCDF) Files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pkeech/stig_parser",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'xmltodict'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
