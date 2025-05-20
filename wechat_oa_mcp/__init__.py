"""
微信公众号MCP服务器源代码包

此 MCP 服务器仅限研究用途，禁止用于商业目的。
"""

# 导入所有公开API
from wechat_oa_mcp.server import (
    WeChat_get_access_token,
    WeChat_create_draft,
    WeChat_publish_draft,
    WeChat_del_draft,
    WeChat_del_material,
    run
)

__all__ = [
    'WeChat_get_access_token',
    'WeChat_create_draft',
    'WeChat_publish_draft',
    'WeChat_del_draft',
    'WeChat_del_material',
    'run'
] 