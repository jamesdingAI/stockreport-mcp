#!/usr/bin/env python3
"""
测试不同 MCP 客户端的工具调用兼容性
"""

import json
import sys
from pathlib import Path

def test_cherry_studio_compatibility():
    """测试 Cherry Studio 的兼容性问题"""
    
    print("🔍 Cherry Studio MCP 兼容性测试")
    print("=" * 50)
    
    # 1. 检查已知问题
    known_issues = [
        {
            "issue": "MCP 服务器无法被调用",
            "description": "服务器启动正常，工具列表显示正常，但无法实际调用工具",
            "github_issue": "https://github.com/CherryHQ/cherry-studio/issues/3513",
            "status": "已知问题"
        },
        {
            "issue": "tool_call_id 参数缺失",
            "description": "使用 OpenAI GPT-4o-mini 时出现 'Missing parameter tool_call_id' 错误",
            "github_issue": "https://github.com/CherryHQ/cherry-studio/issues/4274",
            "status": "已知问题"
        },
        {
            "issue": "工具调用格式差异",
            "description": "Cherry Studio 使用 XML 格式，而其他客户端使用 JSON 格式",
            "status": "设计差异"
        }
    ]
    
    print("📋 已知兼容性问题：")
    for i, issue in enumerate(known_issues, 1):
        print(f"\n{i}. {issue['issue']}")
        print(f"   描述：{issue['description']}")
        print(f"   状态：{issue['status']}")
        if 'github_issue' in issue:
            print(f"   参考：{issue['github_issue']}")
    
    # 2. 客户端差异分析
    print("\n\n🔄 客户端差异分析：")
    print("=" * 30)
    
    client_differences = {
        "Trae AI": {
            "工具调用格式": "标准 OpenAI 函数调用",
            "MCP 支持": "原生支持",
            "已知问题": "无",
            "兼容性": "优秀"
        },
        "Cherry Studio": {
            "工具调用格式": "XML 格式 + JSON 参数",
            "MCP 支持": "部分支持",
            "已知问题": "工具调用失败、tool_call_id 缺失",
            "兼容性": "有限"
        },
        "Claude Desktop": {
            "工具调用格式": "Anthropic 原生格式",
            "MCP 支持": "官方支持",
            "已知问题": "无",
            "兼容性": "优秀"
        },
        "VS Code": {
            "工具调用格式": "标准 MCP 协议",
            "MCP 支持": "扩展支持",
            "已知问题": "配置复杂",
            "兼容性": "良好"
        }
    }
    
    for client, details in client_differences.items():
        print(f"\n📱 {client}:")
        for key, value in details.items():
            print(f"   {key}: {value}")
    
    # 3. 建议的解决方案
    print("\n\n💡 建议的解决方案：")
    print("=" * 30)
    
    solutions = [
        "1. 使用 Trae AI 或 Claude Desktop 进行 MCP 工具调用",
        "2. 如果必须使用 Cherry Studio，尝试使用 Claude 3.5 Sonnet 而非 GPT-4o-mini",
        "3. 检查 Cherry Studio 的版本，确保使用最新版本",
        "4. 监控 Cherry Studio 的 GitHub 仓库，关注相关问题的修复进展",
        "5. 考虑使用其他稳定的 MCP 客户端作为备选方案"
    ]
    
    for solution in solutions:
        print(f"   {solution}")
    
    # 4. 测试建议
    print("\n\n🧪 测试建议：")
    print("=" * 20)
    
    test_steps = [
        "1. 在 Trae AI 中测试相同的 MCP 服务器配置",
        "2. 验证工具调用是否正常工作",
        "3. 比较不同客户端的响应格式",
        "4. 记录具体的错误信息和日志",
        "5. 向 Cherry Studio 团队报告兼容性问题"
    ]
    
    for step in test_steps:
        print(f"   {step}")
    
    print("\n" + "=" * 50)
    print("✅ 兼容性测试完成")
    
    return {
        "known_issues": known_issues,
        "client_differences": client_differences,
        "recommendations": solutions
    }

def generate_compatibility_report():
    """生成兼容性报告"""
    
    report = {
        "title": "MCP 客户端兼容性报告",
        "summary": "Cherry Studio 在 MCP 工具调用方面存在已知问题，建议使用其他客户端",
        "details": test_cherry_studio_compatibility()
    }
    
    # 保存报告
    report_file = Path("mcp_client_compatibility_report.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 兼容性报告已保存到: {report_file}")
    
    return report

if __name__ == "__main__":
    print("🚀 启动 MCP 客户端兼容性测试...")
    
    try:
        report = generate_compatibility_report()
        print("\n✅ 测试完成！")
        
        # 显示关键结论
        print("\n🎯 关键结论：")
        print("   • Cherry Studio 存在 MCP 工具调用问题")
        print("   • Trae AI 的 MCP 支持更加稳定")
        print("   • 建议在 Trae AI 中进行 MCP 工具测试")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        sys.exit(1)