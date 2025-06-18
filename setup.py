from setuptools import setup, find_packages

setup(
    name="lol_sim_env",
    version="0.1.0",
    description="League of Legends Simulated Laning Environment for Reinforcement Learning",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "gymnasium>=0.29.0",
        "pyyaml>=6.0",
    ],
    python_requires=">=3.8",
    author="Project Taric",
    author_email="",
    url="https://github.com/Estaed/Lol_Sim_Env",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 