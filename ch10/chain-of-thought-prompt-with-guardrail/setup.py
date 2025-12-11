from setuptools import find_packages, setup

setup(
    name="coffee-order-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.109.0",
        "pydantic>=2.6.0",
        "mangum>=0.17.0",
        "uvicorn>=0.27.0",
        "pynamodb>=5.5.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-mock>=3.12.0",
            "httpx>=0.26.0",
            "pre-commit>=3.6.0",
            "black>=24.1.0",
            "isort>=5.13.2",
            "ruff>=0.2.0",
            "mypy>=1.8.0",
            "bandit>=1.7.7",
        ],
    },
)
