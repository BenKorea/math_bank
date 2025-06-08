# setup.py
from setuptools import setup, find_packages

setup(
    name="mathbank",
    version="0.1.0",
    description="중학교 수학문제 자동 변환 및 관리 시스템",
    author="사용자이름",
    packages=find_packages(include=["modules", "modules.*"]),
    install_requires=[
        "pyyaml",
        # 여기에 추가 의존성 입력 가능
    ],
    python_requires=">=3.8",
)
