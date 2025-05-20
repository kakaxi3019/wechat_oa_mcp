from setuptools import setup, find_packages
import os

# 读取README.md文件内容作为长描述
current_dir = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(current_dir, "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "微信公众号MCP Server - 此 MCP 服务器仅限研究用途，禁止用于商业目的。"

setup(
    name="wechat_oa_mcp",
    version="0.1.0",
    author="Jupiter",
    author_email="jupiter3019@163.com",
    description="微信公众号MCP Server - 此 MCP 服务器仅限研究用途，禁止用于商业目的。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "fastmcp",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "wechat-oa-mcp=wechat_oa_mcp.cli:main",
        ],
    },
    include_package_data=True,
) 