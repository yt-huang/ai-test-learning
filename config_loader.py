#!/usr/bin/env python3
"""
配置加载器 - 按优先级尝试多个配置文件
优先级顺序：
1. 系统环境变量
2. .env.local (本地配置，最高优先级)
3. .env (通用环境变量配置)
4. config.json (JSON 配置)
5. config.yaml (YAML 配置)
"""

import os
import json
from pathlib import Path


def load_config():
    """加载配置，按优先级尝试多个来源"""
    config = {}

    # 1. 首先尝试 .env.local (本地开发配置，优先级最高)
    if Path(".env.local").exists():
        print("📄 加载配置: .env.local")
        config.update(_load_env_file(".env.local"))
        if _has_nvidia_config(config):
            return config

    # 2. 尝试 .env (通用环境变量配置)
    if Path(".env").exists():
        print("📄 加载配置: .env")
        config.update(_load_env_file(".env"))
        if _has_nvidia_config(config):
            return config

    # 3. 尝试 config.json
    if Path("config.json").exists():
        print("📄 加载配置: config.json")
        config.update(_load_json_config("config.json"))
        if _has_nvidia_config(config):
            return config

    # 4. 尝试 config.yaml
    if Path("config.yaml").exists():
        print("📄 加载配置: config.yaml")
        config.update(_load_yaml_config("config.yaml"))
        if _has_nvidia_config(config):
            return config

    # 5. 最后检查系统环境变量
    print("📄 加载配置: 系统环境变量")
    config.update(_load_from_env_vars())

    return config


def _load_env_file(filepath):
    """加载 .env 文件"""
    config = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip().strip('"\'')
    except Exception as e:
        print(f"⚠️  读取 {filepath} 失败: {e}")
    return config


def _load_json_config(filepath):
    """加载 JSON 配置文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 将嵌套的 nvidia 配置扁平化
            if 'nvidia' in data:
                return {
                    'NVIDIA_API_KEY': data['nvidia'].get('api_key'),
                    'NVIDIA_BASE_URL': data['nvidia'].get('base_url'),
                    'NVIDIA_MODEL': data['nvidia'].get('model'),
                    'NVIDIA_TEMPERATURE': str(data['nvidia'].get('temperature', 0.7)),
                }
    except Exception as e:
        print(f"⚠️  读取 {filepath} 失败: {e}")
    return {}


def _load_yaml_config(filepath):
    """加载 YAML 配置文件"""
    try:
        import yaml
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if data and 'nvidia' in data:
                return {
                    'NVIDIA_API_KEY': data['nvidia'].get('api_key'),
                    'NVIDIA_BASE_URL': data['nvidia'].get('base_url'),
                    'NVIDIA_MODEL': data['nvidia'].get('model'),
                    'NVIDIA_TEMPERATURE': str(data['nvidia'].get('temperature', 0.7)),
                }
    except ImportError:
        print("⚠️  未安装 PyYAML，跳过 YAML 配置")
    except Exception as e:
        print(f"⚠️  读取 {filepath} 失败: {e}")
    return {}


def _load_from_env_vars():
    """从系统环境变量加载"""
    return {
        'NVIDIA_API_KEY': os.getenv('NVIDIA_API_KEY'),
        'NVIDIA_BASE_URL': os.getenv('NVIDIA_BASE_URL', 'https://integrate.api.nvidia.com/v1'),
        'NVIDIA_MODEL': os.getenv('NVIDIA_MODEL', 'moonshotai/kimi-k2.5'),
        'NVIDIA_TEMPERATURE': os.getenv('NVIDIA_TEMPERATURE', '0.7'),
    }


def _has_nvidia_config(config):
    """检查配置中是否包含 NVIDIA API key"""
    return bool(config.get('NVIDIA_API_KEY'))


def get_nvidia_config():
    """获取 NVIDIA 配置，用于创建 LLM 实例"""
    config = load_config()

    api_key = config.get('NVIDIA_API_KEY')
    if not api_key:
        raise ValueError("未找到 NVIDIA_API_KEY，请检查配置文件")

    return {
        'api_key': api_key,
        'base_url': config.get('NVIDIA_BASE_URL', 'https://integrate.api.nvidia.com/v1'),
        'model': config.get('NVIDIA_MODEL', 'moonshotai/kimi-k2.5'),
        'temperature': float(config.get('NVIDIA_TEMPERATURE', 0.7)),
    }


# 测试加载
if __name__ == "__main__":
    print("🔧 测试配置加载...\n")
    try:
        config = get_nvidia_config()
        print("\n✅ 配置加载成功:")
        print(f"   模型: {config['model']}")
        print(f"   API URL: {config['base_url']}")
        print(f"   Temperature: {config['temperature']}")
        print(f"   API Key: {config['api_key'][:20]}...")
    except ValueError as e:
        print(f"\n❌ {e}")
        print("\n可用配置文件:")
        for f in ['.env.local', '.env', 'config.json', 'config.yaml']:
            exists = "✓" if Path(f).exists() else "✗"
            print(f"   [{exists}] {f}")
