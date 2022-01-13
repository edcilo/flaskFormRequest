import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flaskFormRequest",
    version="0.0.2",
    author="edcilo",
    description="Request validator for flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['flaskFormRequest'],
    exclude=["test"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    include_package_data=True,
    package_dir={'':'src'},
)
