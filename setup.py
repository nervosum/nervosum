from setuptools import find_packages, setup

setup(
    name="nervosum",
    version="1.0",
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={"console_scripts": ["nervosum = nervosum.cli.main:main"]},
    package_data={"nervosum": ["templates/**/*", "templates/**/*.txt"]},
    install_requires=[
        "pyyaml",
        "jinja2",
        "docker",
        "timeago",
        "pydantic",
        "python-dateutil",
    ],
    extras_require={
        "dev": ["pre-commit", "pytest", "pytest-cov", "pytest-mock"]
    },
)
