from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smart-automation-utils",
    version="0.2.0",
    author="dhiraj",
    author_email="gowebdk@gmail.com",
    description="A python package for automation developers working with Selenium and Appium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.dhirajdas.dev",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "selenium>=4.0.0",
        "Appium-Python-Client",
        "psutil",
        "webdriver-manager",
        "pytest",
        "pytest-glow-report",
        "waitless"
    ],
)
