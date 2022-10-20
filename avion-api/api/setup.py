import setuptools

setuptools.setup(
    name="avion-api",
    version="1.0.0",
    url="",
    author="Diddi Oskarsson",
    author_email="diddi@diddi.se",
    description="Avion API",
    long_description="Avion API",
    long_description_content_type="text/markdown",
    packages=setuptools.find_namespace_packages(include=["avion.api.*"]),
    include_package_data=True,
    license="MIT",
    install_requires=[
        "Flask>=2.0.3, <=2.1.3",
        "flask-restx",
        "werkzeug >=2.1, <2.2",
        "marshmallow",
        "Flask-CORS"
    ],
    extras_require={
        "test": [
            "mockito",
            "pylint>=2.15.4"
        ]  # Dependencies for testing go here
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
