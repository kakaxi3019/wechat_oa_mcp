"""
微信公众号MCP服务器核心实现

此 MCP 服务器仅限研究用途，禁止用于商业目的。

使用限制：
为了分散压力，每个IP每分钟内最多能调用同一接口五次。

IP白名单配置：
根据微信公众号开发接口管理规定，通过开发者ID及密码调用获取access_token接口时，
需要设置访问来源IP为白名单。请将以下IP添加至微信公众号-设置与开发-开发接口管理-IP白名单：
106.15.125.133
"""

from mcp.server.fastmcp import FastMCP
import requests
from typing import Dict, Any

# 定义基础URL常量
BASE_URL = "http://106.15.125.133"

# 创建FastMCP服务器实例
mcp = FastMCP()

# 实现微信API功能
@mcp.tool()
def WeChat_create_draft(args) -> Dict[str, Any]:
    """
    创建微信公众号草稿
    
    Metadata:
    - input: access_token, image_url, title, content, author, digest, content_source_url, need_open_comment
    - output: success, error, draft_media_id, image_media_id
    
    参数说明:
    - access_token: 接口凭证
    - image_url: 封面图片URL
    - title: 文章标题
    - content: 图文消息内容，支持HTML，<2万字符，<1M
    - author: (可选)作者名称
    - digest: (可选)摘要，默认取正文前54字
    - content_source_url: (可选)原文URL
    - need_open_comment: (可选)0关闭评论(默认)，1开启
    """
    # 检查参数格式，支持直接传入字典或通过args.input获取
    if hasattr(args, 'input'):
        input_params = args.input
        logger = args.logger
    else:
        # 直接使用args作为输入参数
        input_params = args
        # 如果没有logger，创建一个简单的print函数替代
        logger = type('', (), {'debug': print, 'error': print})
    
    # 构建请求参数
    payload = {
        "access_token": input_params.get("access_token", ""),
        "image_url": input_params.get("image_url", ""),
        "title": input_params.get("title", ""),
        "content": input_params.get("content", "")
    }

    if hasattr(input_params, 'author') and input_params.author:
        payload['author'] = input_params.author
    elif input_params.get("author"):
        payload['author'] = input_params.get("author")
        
    if hasattr(input_params, 'digest') and input_params.digest:
        payload['digest'] = input_params.digest
    elif input_params.get("digest"):
        payload['digest'] = input_params.get("digest")
        
    if hasattr(input_params, 'content_source_url') and input_params.content_source_url:
        payload['content_source_url'] = input_params.content_source_url
    elif input_params.get("content_source_url"):
        payload['content_source_url'] = input_params.get("content_source_url")
        
    if hasattr(input_params, 'need_open_comment') and input_params.need_open_comment:
        payload['need_open_comment'] = input_params.need_open_comment
    elif input_params.get("need_open_comment"):
        payload['need_open_comment'] = input_params.get("need_open_comment")
    
    try:
        # 发送POST请求
        response = requests.post(
            url=f"{BASE_URL}:8001/create_wechat_draft",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json=payload,
            timeout=10
        )
        
        # 记录调试信息
        logger.debug(f"Request payload: {payload}")
        logger.debug(f"Response status: {response.status_code}")
        
        # 处理响应
        response.raise_for_status()

        # 解析结果
        result = response.json()
        if "draft_media_id" not in result:
            raise ValueError("响应中缺少draft_media_id字段")

        return {
            "success": True,
            "error": None,
            "draft_media_id": result["draft_media_id"],
            "image_media_id": result["image_media_id"]
        }
        
    except requests.exceptions.RequestException as e:
        # 记录错误信息
        logger.error(f"API请求失败: {str(e)}")
        return {
            "success": False,
            "error": f"网络请求异常: {str(e)}",
            "response": None
        }
    except Exception as e:
        # 处理未知异常
        logger.error(f"未知错误: {str(e)}")
        return {
            "success": False,
            "error": f"系统异常: {str(e)}",
            "response": None
        }

@mcp.tool()
def WeChat_del_draft(args) -> Dict[str, Any]:
    """
    删除微信公众号草稿
    
    Metadata:
    - input: access_token, media_id
    - output: success, error, errcode, errmsg
    
    参数说明:
    - access_token: 接口凭证
    - media_id: 草稿ID，即WeChat_create_draft返回的draft_media_id
    """
    # 检查参数格式，支持直接传入字典或通过args.input获取
    if hasattr(args, 'input'):
        input_params = args.input
        logger = args.logger
    else:
        # 直接使用args作为输入参数
        input_params = args
        # 如果没有logger，创建一个简单的print函数替代
        logger = type('', (), {'debug': print, 'error': print})

    try:
        # 发送删除请求
        response = requests.post(
            url=f"{BASE_URL}:8004/del_wechat_draft",
            headers={"Content-Type": "application/json"},
            json={
                "access_token": input_params.get("access_token", ""),
                "media_id": input_params.get("media_id", "")
            },
            timeout=12
        )

        # 记录调试信息
        logger.debug(f"请求地址: {response.url}")
        logger.debug(f"响应原始内容: {response.text}")

        # 处理HTTP状态码
        response.raise_for_status()
        
        # 解析业务响应
        result = response.json()
        if result.get("errcode", 0) != 0:
            raise ValueError(f"业务错误: {result.get('errmsg', '未知错误')}")
        
        return {
            "success": True,
            "error": None,
            "errcode": result.get("errcode"),
            "errmsg": result.get("errmsg") 
        }

    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP异常 {e.response.status_code}"
        logger.error(f"{error_msg} - 响应内容: {e.response.text}")
        return {
            "success": False,
            "error": error_msg,
            "errcode": None,
            "errmsg": None
        }
    except ValueError as e:
        logger.error(f"业务逻辑错误: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "errcode": None,
            "errmsg": None
        }
    except Exception as e:
        logger.error(f"系统异常: {str(e)}")
        return {
            "success": False,
            "error": f"系统错误: {str(e)}",
            "errcode": None,
            "errmsg": None
        }

@mcp.tool()
def WeChat_del_material(args) -> Dict[str, Any]:
    """
    删除微信公众号永久素材
    
    Metadata:
    - input: access_token, media_id
    - output: success, error, errcode, errmsg
    
    参数说明:
    - access_token: 接口凭证
    - media_id: 素材ID，即WeChat_create_draft返回的image_media_id
    """
    # 检查参数格式，支持直接传入字典或通过args.input获取
    if hasattr(args, 'input'):
        input_params = args.input
        logger = args.logger
    else:
        # 直接使用args作为输入参数
        input_params = args
        # 如果没有logger，创建一个简单的print函数替代
        logger = type('', (), {'debug': print, 'error': print})

    try:
        # 发送删除请求
        response = requests.post(
            url=f"{BASE_URL}:8003/del_wechat_material",
            headers={"Content-Type": "application/json"},
            json={
                "access_token": input_params.get("access_token", ""),
                "media_id": input_params.get("media_id", "")
            },
            timeout=12
        )

        # 记录调试信息
        logger.debug(f"请求地址: {response.url}")
        logger.debug(f"响应原始内容: {response.text}")

        # 处理HTTP状态码
        response.raise_for_status()
        
        # 解析业务响应
        result = response.json()
        if result.get("errcode", 0) != 0:
            raise ValueError(f"业务错误: {result.get('errmsg', '未知错误')}")
        
        return {
            "success": True,
            "error": None,
            "errcode": result.get("errcode"),
            "errmsg": result.get("errmsg") 
        }

    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP异常 {e.response.status_code}"
        logger.error(f"{error_msg} - 响应内容: {e.response.text}")
        return {
            "success": False,
            "error": error_msg,
            "errcode": None,
            "errmsg": None
        }
    except ValueError as e:
        logger.error(f"业务逻辑错误: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "errcode": None,
            "errmsg": None
        }
    except Exception as e:
        logger.error(f"系统异常: {str(e)}")
        return {
            "success": False,
            "error": f"系统错误: {str(e)}",
            "errcode": None,
            "errmsg": None
        }

@mcp.tool()
def WeChat_get_access_token(args) -> Dict[str, Any]:
    """
    获取微信公众号Access Token
    
    Metadata:
    - input: AppID, AppSecret
    - output: success, error, access_token, expires_in
    
    参数说明:
    - AppID: 公众号唯一凭证
    - AppSecret: 公众号凭证密钥
    - expires_in: 凭证有效时间(秒)，默认7200
    """
    # 处理输入参数格式，支持直接字典或args.input
    if hasattr(args, 'input'):
        input_params = args.input
        logger = args.logger
    else:
        input_params = args
        logger = type('', (), {'debug': print, 'error': print})
    
    try:
        # 发送获取access_token的请求
        response = requests.post(
            url=f"{BASE_URL}:8000/get_wechat_token",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={
                "appid": input_params.get("AppID", ""),
                "appsecret": input_params.get("AppSecret", "")
            },
            timeout=10
        )
        
        # 记录调试信息
        logger.debug(f"请求地址: {response.url}")
        logger.debug(f"响应状态: {response.status_code}")
        
        # 处理HTTP响应状态
        response.raise_for_status()
        
        # 解析业务层响应
        result = response.json()
        if not result.get("access_token"):
            raise ValueError("未能获取有效的access_token")
        
        # 返回成功结果
        return {
            "success": True,
            "error": None,
            "access_token": result.get("access_token"),
            "expires_in": result.get("expires_in", 7200)
        }
        
    except requests.exceptions.RequestException as e:
        # 处理网络类错误
        logger.error(f"HTTP请求失败: {str(e)}")
        return {
            "success": False,
            "error": f"HTTP请求异常: {str(e)}",
            "access_token": None,
            "expires_in": None
        }
    except ValueError as e:
        # 处理业务逻辑错误
        logger.error(f"业务错误: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "access_token": None,
            "expires_in": None
        }
    except Exception as e:
        # 处理未知错误
        logger.error(f"未知错误: {str(e)}")
        return {
            "success": False,
            "error": f"系统错误: {str(e)}",
            "access_token": None,
            "expires_in": None
        }

@mcp.tool()
def WeChat_publish_draft(args) -> Dict[str, Any]:
    """
    发布微信公众号草稿
    
    Metadata:
    - input: access_token, draft_media_id
    - output: success, error, errmsg, publish_id
    
    参数说明:
    - access_token: 接口凭证
    - draft_media_id: 草稿ID，即WeChat_create_draft返回的draft_media_id
    - publish_id: 发布任务ID
    """
    # 检查参数格式，支持直接传入字典或通过args.input获取
    if hasattr(args, 'input'):
        input_params = args.input
        logger = args.logger
    else:
        # 直接使用args作为输入参数
        input_params = args
        # 如果没有logger，创建一个简单的print函数替代
        logger = type('', (), {'debug': print, 'error': print})

    try:
        # 构建请求参数
        payload = {
            "access_token": input_params.get("access_token", ""),
            "media_id": input_params.get("draft_media_id", "")
        }
        
        # 发送请求
        response = requests.post(
            url=f"{BASE_URL}:8002/publish_wechat_draft",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=15  # 发布可能需要较长时间
        )
        
        # 记录调试信息
        logger.debug(f"请求载荷: {payload}")
        logger.debug(f"响应状态: {response.status_code}")
        
        # 处理HTTP状态码
        response.raise_for_status()
        
        # 解析业务响应
        result = response.json()
        if "publish_id" not in result and "msg_id" not in result:
            raise ValueError("响应缺少publish_id或msg_id字段")
        
        # 返回成功结果
        return {
            "success": True,
            "error": None,
            "errmsg": result.get("errmsg"),
            "publish_id": result.get("publish_id", result.get("msg_id"))
        }
        
    except requests.exceptions.RequestException as e:
        # 处理HTTP请求错误
        logger.error(f"HTTP请求失败: {str(e)}")
        return {
            "success": False,
            "error": f"网络请求异常: {str(e)}",
            "publish_id": None
        }
    except ValueError as e:
        # 处理业务逻辑错误
        logger.error(f"业务错误: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "publish_id": None
        }
    except Exception as e:
        # 处理未知错误
        logger.error(f"未知错误: {str(e)}")
        return {
            "success": False,
            "error": f"系统错误: {str(e)}",
            "publish_id": None
        }

def run(transport="sse", port=None, debug=False):
    """
    启动WeChat OA MCP服务器
    
    参数:
        transport: 通信协议，支持 'sse'(Server-Sent Events), 'stdio'(标准输入输出), 'streamable-http'(HTTP长轮询)
        port: 服务器端口，如果不指定则使用默认端口
        debug: 是否启用调试模式，开启详细日志
    """
    # 只有在非stdio模式或debug模式下才输出启动信息
    if transport != "stdio" or debug:
        print(f"启动WeChat OA MCP服务器，通信协议: {transport}")
        if port is not None:
            print(f"使用自定义端口: {port}")
    
    # 确定使用哪个MCP实例
    if port is None:
        # 如果未指定端口，直接使用全局mcp实例
        server = mcp
    else:
        # 如果指定了端口，创建新实例并设置端口
        server = FastMCP(port=port)
        
        # 注册所有工具函数到新创建的服务器实例
        for tool_name in [
            "WeChat_get_access_token",
            "WeChat_create_draft", 
            "WeChat_publish_draft",
            "WeChat_del_draft", 
            "WeChat_del_material"
        ]:
            if tool_name in globals():
                server.add_tool(globals()[tool_name])
    
    try:
        # 使用确定的服务器实例运行
        server.run(transport=transport)
    except KeyboardInterrupt:
        if transport != "stdio" or debug:
            print("服务被用户中断")
    except Exception as e:
        if transport != "stdio" or debug:
            print(f"服务启动失败: {str(e)}")
        raise 