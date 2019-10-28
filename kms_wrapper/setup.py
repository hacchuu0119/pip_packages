import setuptools

setuptools.setup(
    name="kms_wrapper",
    version="0.1.0",
    packages=setuptools.find_packages(),
    install_requires=[
        "pycryptodomex",
        "boto3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7-3.8",
        "Operating System :: OS Independent",
    ]
)