#!/usr/bin/env python
"""
简单的微信公众号OA MCP工具使用示例

免责声明：此 MCP 服务器仅限研究用途，禁止用于商业目的。
使用限制：为了分散服务器压力，每个IP每分钟内最多能调用同一接口五次。

IP白名单配置：
根据微信公众号开发接口管理规定，通过开发者ID及密码调用获取access_token接口时，
需要设置访问来源IP为白名单。请将以下IP添加至微信公众号-设置与开发-开发接口管理-IP白名单：
106.15.125.133
"""
import sys
import os
import time

# 导入微信MCP工具API
try:
    # 如果已经安装为包，直接导入
    from wechat_oa_mcp import (
        WeChat_get_access_token,
        WeChat_create_draft,
        WeChat_publish_draft,
        WeChat_del_draft,
        WeChat_del_material
    )
except ImportError:
    # 如果未安装，尝试从当前目录导入
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from wechat_oa_mcp import (
        WeChat_get_access_token,
        WeChat_create_draft,
        WeChat_publish_draft,
        WeChat_del_draft,
        WeChat_del_material
    )

def main():
    # 示例AppID和AppSecret (需要替换为有效值)
    app_id = "your_app_id" 
    app_secret = "your_app_secret"
    
    print("1. 获取Access Token...")
    token_result = WeChat_get_access_token({
        "AppID": app_id,
        "AppSecret": app_secret
    })
    
    if not token_result["success"]:
        print(f"Error: {token_result['error']}")
        sys.exit(1)
    
    access_token = token_result["access_token"]
    print(f"Access Token: {access_token[:10]}...")
    
    print("\n2. 创建草稿...")
    draft_result = WeChat_create_draft({
        "access_token": access_token,
        "image_url": "https://example.com/image.jpg",
        "title": "测试文章 - " + time.strftime("%Y-%m-%d %H:%M"),
        "content": "<p>这是通过WeChat OA MCP工具创建的测试文章</p>",
        "author": "MCP测试"
    })
    
    if not draft_result["success"]:
        print(f"创建草稿失败: {draft_result['error']}")
        sys.exit(1)
    
    draft_id = draft_result["draft_media_id"]
    image_id = draft_result["image_media_id"]
    print(f"草稿ID: {draft_id}")
    print(f"图片ID: {image_id}")
    
    # 是否需要发布草稿
    should_publish = input("\n是否要发布这篇草稿? (y/n): ").lower() == 'y'
    
    if should_publish:
        print("\n3. 发布草稿...")
        publish_result = WeChat_publish_draft({
            "access_token": access_token,
            "draft_media_id": draft_id
        })
        
        if publish_result["success"]:
            print(f"发布成功! 发布ID: {publish_result['publish_id']}")
        else:
            print(f"发布失败: {publish_result['error']}")
    
    # 是否需要删除草稿
    should_del_draft = input("\n是否要删除这篇草稿? (y/n): ").lower() == 'y'
    
    if should_del_draft:
        print("\n4. 删除草稿...")
        del_draft_result = WeChat_del_draft({
            "access_token": access_token,
            "media_id": draft_id
        })
        
        if del_draft_result["success"]:
            print(f"删除草稿成功! 结果: {del_draft_result['errmsg']}")
        else:
            print(f"删除草稿失败: {del_draft_result['error']}")
    
    # 是否需要删除素材
    should_del_material = input("\n是否要删除图片素材? (y/n): ").lower() == 'y'
    
    if should_del_material:
        print("\n5. 删除素材(图片)...")
        del_material_result = WeChat_del_material({
            "access_token": access_token,
            "media_id": image_id
        })
        
        if del_material_result["success"]:
            print(f"删除素材成功! 结果: {del_material_result['errmsg']}")
        else:
            print(f"删除素材失败: {del_material_result['error']}")
    
    print("\n演示完成!")

if __name__ == "__main__":
    main() 