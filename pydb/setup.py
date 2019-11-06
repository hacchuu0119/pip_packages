import setuptools

setuptools.setup(
    name="pydb",
    version="0.1.1",
    packages=setuptools.find_packages(),
    install_requires=[
        "sqlalchemy",
        "mysqlclient",
        "cx_Oracle",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ]
)