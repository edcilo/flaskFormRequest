import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flaskFormRequest",
    version="0.0.1",
    author="edcilo",
    description="Request validator for flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    py_modules=["flaskFormRequest"],
    package_dir={'':'./'},
    install_requires=[
        'flask',
    ],
)
