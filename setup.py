from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="ai-travel-agent",
    version="0.1.0",
    author="Deep",
    description="A travel agent that uses AI to help you plan your trip",
    packages=find_packages(),
    install_requires=requirements,
)