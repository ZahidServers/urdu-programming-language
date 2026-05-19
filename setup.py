"""Setup script for the Urdu Programming Language."""

from setuptools import setup, find_packages
from pathlib import Path

long_description = Path("README.md").read_text(encoding="utf-8") if Path("README.md").exists() else ""

setup(
    name="urdu-lang",
    version="1.0.0",
    author="Mohammed Zahid Wadiwale",
    author_email="zahid.wadiwale1234@gmail.com",
    description="اردو پروگرامنگ لینگویج — Urdu Programming Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zahid-wadiwale/urdu-lang",
    packages=find_packages(),
    package_data={
        "urdu": ["*.py"],
        "urdu.runtime": ["*.py"],
    },
    python_requires=">=3.9",
    install_requires=[
        # Core — no extra installs needed for basic usage
    ],
    extras_require={
        "gui": [],                              # tkinter is built-in
        "mysql": ["mysql-connector-python"],
        "postgresql": ["psycopg2-binary"],
        "mongodb": ["pymongo"],
        "firebase": ["firebase-admin"],
        "cassandra": ["cassandra-driver"],
        "fastapi": ["fastapi", "uvicorn[standard]"],
        "flask": ["flask"],
        "django": ["django"],
        "ml": ["tensorflow", "scikit-learn", "numpy", "pandas"],
        "llm": ["llama-cpp-python"],
        "http": ["aiohttp", "requests"],
        "websockets": ["websockets"],
        "data": ["numpy", "pandas", "matplotlib"],
        "all": [
            "mysql-connector-python",
            "psycopg2-binary",
            "pymongo",
            "firebase-admin",
            "cassandra-driver",
            "fastapi",
            "uvicorn[standard]",
            "flask",
            "django",
            "scikit-learn",
            "numpy",
            "pandas",
            "matplotlib",
            "aiohttp",
            "requests",
            "websockets",
        ],
    },
    entry_points={
        "console_scripts": [
            "urdu=urdu.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Interpreters",
        "Natural Language :: Urdu",
    ],
    keywords=[
        "urdu", "programming language", "اردو", "پروگرامنگ",
        "compiler", "transpiler", "education",
    ],
    project_urls={
        "Developer": "https://github.com/zahid-wadiwale",
    },
)
