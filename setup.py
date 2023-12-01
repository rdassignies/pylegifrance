from setuptools import setup, find_packages

with open("readme.md", 'r') as f:
    long_description = f.read()

setup(
    name="pylegifrance",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2",
        "requests",
        "PyYAML"
    ],
    description="Librairie qui fournit des fonctions simples pour rechercher dans legifrance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/rdassignies/pylegifrance',
    author="Raphaël d'Assignies",
    author_email="rdassignies@protonmail.ch",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.8",
)
