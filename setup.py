from setuptools import setup, find_packages

setup(
    name="ai_prescription_verifier",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Core Dependencies
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
        "python-multipart>=0.0.6",
        
        # Data Processing
        "pandas>=2.1.3",
        "numpy>=1.24.3",
        
        # Environment
        "python-dotenv>=1.0.0",
        
        # AI/ML
        "transformers>=4.36.2",
        "torch>=2.1.2",
        "sentencepiece>=0.1.99",
        "accelerate>=0.24.1",
        
        # IBM Watson
        "ibm-watson>=7.0.1",
        "ibm-cloud-sdk-core>=3.16.1"
    ],
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI Prescription Verifier - A system for verifying medical prescriptions using AI",
    keywords="ai medical prescription verification healthcare",
    url="https://github.com/yourusername/ai-prescription-verifier"
)
