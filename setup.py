import setuptools
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="emtask",
        version="0.0.1a6",
        author="David Alvarez Garcia",
        author_email="david.avgarcia@gmail.com",
        description="A provides a set of scripts for autmate em dev tasks",
        long_description=long_description,
        long_description_content_type="text/markdown",
        keywords="cli em code-automation",
        url="https://github.com/vecin2/ccdev",
        packages=setuptools.find_packages(exclude=["nubia_test"]),
        python_requires=">=3.6",
        install_requires=REQUIREMENTS,
        classifiers=[
            "Environment :: Console",
            "Programming Language :: Python :: 3.6",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        entry_points = {
            'console_scripts': [
                'em=em.__main__:main'
                ],
            }
        )
