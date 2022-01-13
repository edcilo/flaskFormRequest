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
    packages=setuptools.find_packages(),
    exclude=["test"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    py_modules=["flaskFormRequest"],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
