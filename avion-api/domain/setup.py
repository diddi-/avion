import setuptools

setuptools.setup(
    name="avion",
    version="1.0.0",
    url="",
    author="Diddi Oskarsson",
    author_email="diddi@diddi.se",
    description="Avion",
    long_description="Avion",
    long_description_content_type="text/markdown",
    packages=setuptools.find_namespace_packages(include=["avion.*"]),
    include_package_data=True,
    license="MIT",
    install_requires=[
        "flask-jwt-extended"
    ],
    extras_require={
        "test": [
            "mockito"
        ]  # Dependencies for testing go here
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
