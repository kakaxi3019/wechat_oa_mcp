#!/usr/bin/env python
"""
WeChat OA MCP 服务器命令行入口模块
提供便捷的启动服务器和调用微信公众号API的功能
"""

import argparse
import sys
import os
from wechat_oa_mcp.server import run

def main():
    """
    命令行入口点函数
    启动WeChat OA MCP服务器
    """
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="WeChat OA MCP 服务器")
    parser.add_argument("--port", type=int, help="指定服务器端口")
    parser.add_argument("--transport", type=str, choices=["sse", "stdio", "streamable-http"], 
                      default="sse", help="指定通信协议")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    args = parser.parse_args()
    
    # 检测是否通过管道方式运行（如 npx inspector）
    is_piped = not os.isatty(sys.stdin.fileno()) or not os.isatty(sys.stdout.fileno())
    
    # 如果是通过管道运行，则强制使用 stdio 传输协议
    transport = "stdio" if is_piped else args.transport
    
    if is_piped:
        # 直接运行，不打印额外信息以免干扰通信
        run(transport=transport, port=args.port, debug=args.debug)
    else:
        # 正常启动服务器
        try:
            run(transport=transport, port=args.port, debug=args.debug)
        except KeyboardInterrupt:
            print("\n服务器已停止")
        except Exception as e:
            print(f"服务器异常: {str(e)}")
            return 1
    return 0

if __name__ == "__main__":
    main() 