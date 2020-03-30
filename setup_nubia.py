





setuptools.setup(
    name="python-nubia",
    version=get_version(),
    author="Ahmed Soliman",
    author_email="asoli@fb.com",
    description="A framework for building beautiful shells",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords="cli shell interactive framework",
    url="https://github.com/facebookincubator/python-nubia",
    packages=setuptools.find_packages(exclude=["sample", "docs", "tests"]),
    python_requires=">=3.6",
    setup_requires=["nose>=1.0", "coverage"],
    tests_require=["nose>=1.0", "dataclasses;python_version<'3.7'"],
    entry_points={"console_scripts": ["_nubia_complete = nubia_complete.main:main"]},
    install_requires=reqs,
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ),
)
