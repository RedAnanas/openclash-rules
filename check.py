"""检查本配置包的引用、个人规则与公共下载地址，不请求机场订阅。"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import urllib.error
import urllib.request

import yaml


class UniqueLoader(yaml.SafeLoader):
    """拒绝重复字段，避免后面的配置静默覆盖前面的配置。"""


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in result:
            raise ValueError(f"YAML 字段重复：{key}")
        result[key] = loader.construct_object(value_node)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load(path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)


def validate(config, root):
    errors = []
    groups = config.get("proxy-groups", [])
    names = [group["name"] for group in groups]
    if len(names) != len(set(names)):
        errors.append("策略组名称重复")
    targets = set(names) | {"DIRECT", "REJECT"}
    providers = config.get("rule-providers", {})
    node_providers = config.get("proxy-providers", {})
    for group in groups:
        for target in group.get("proxies", []):
            if target not in targets:
                errors.append(f"策略组 {group['name']} 引用了不存在的出口 {target}")
        for name in group.get("use", []):
            if name not in node_providers:
                errors.append(f"策略组 {group['name']} 引用了不存在的节点源 {name}")

    graph = {group["name"]: group.get("proxies", []) for group in groups}
    visiting, visited = set(), set()

    def visit(name):
        if name in visiting:
            errors.append(f"策略组存在循环引用：{name}")
            return
        if name in visited or name not in graph:
            return
        visiting.add(name)
        for target in graph[name]:
            visit(target)
        visiting.remove(name)
        visited.add(name)

    for name in graph:
        visit(name)

    rules = config.get("rules", [])
    used = set()
    if not rules or rules[-1] != "MATCH,漏网之鱼":
        errors.append("最后一条必须为 MATCH,漏网之鱼")
    for rule in rules:
        parts = rule.split(",")
        if parts[0] == "RULE-SET" and len(parts) in (3, 4):
            used.add(parts[1])
            if parts[1] not in providers:
                errors.append(f"规则引用了不存在的规则集 {parts[1]}")
        elif parts[0] != "MATCH" or len(parts) != 2:
            errors.append(f"主规则格式不符合本包约定：{rule}")
            continue
        target = parts[2] if parts[0] == "RULE-SET" else parts[1]
        if target not in targets:
            errors.append(f"规则引用了不存在的出口 {target}")
    for name in providers.keys() - used:
        errors.append(f"规则集没有被使用：{name}")

    paths = set()
    for name, provider in providers.items():
        if provider["type"] == "inline":
            if not isinstance(provider.get("payload"), list):
                errors.append(f"内嵌规则必须提供列表：{name}")
            continue
        relative = Path(provider["path"])
        if relative.parent != Path("rule_provider") or not relative.name.startswith("msm-"):
            errors.append(f"必须使用 OpenClash 原生规则目录和 msm- 前缀：{name}")
        path = (root / provider["path"]).resolve()
        if not path.is_relative_to(root.resolve()):
            errors.append(f"规则集路径超出配置目录：{name}")
            continue
        if path in paths:
            errors.append(f"多个规则集使用同一缓存或文件：{name}")
        paths.add(path)
        if provider["type"] == "http":
            if not provider.get("url", "").startswith("https://"):
                errors.append(f"公共规则地址必须使用 HTTPS：{name}")
            continue
        try:
            payload = load(path)["payload"]
            if not isinstance(payload, list):
                raise ValueError("payload 必须是列表")
            for rule in payload:
                parts = rule.split(",")
                if len(parts) not in (2, 3) or (len(parts) == 3 and parts[-1] != "no-resolve"):
                    raise ValueError("个人规则只写匹配条件，不写出口")
                if parts[0] not in {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR", "IP-CIDR6", "DST-PORT"}:
                    raise ValueError(f"检查工具尚不支持此规则类型：{parts[0]}，请扩展检查并用内核验证")
        except (OSError, ValueError, KeyError, TypeError, AttributeError, yaml.YAMLError) as exc:
            errors.append(f"个人规则 {name} 无效：{exc}")
    return errors


def probe(item):
    name, provider = item
    try:
        request = urllib.request.Request(provider["url"], headers={"User-Agent": "msm-openclash-check"})
        with urllib.request.urlopen(request, timeout=20) as response:
            if not response.read(16):
                return f"{name}：下载内容为空"
        return None
    except (OSError, urllib.error.URLError):
        return f"{name}：下载失败，请检查网络、HTTP 状态和源文件；本工具不自动换源"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path(__file__).resolve().parent / "config.yaml", help="要检查的主配置，默认 config.yaml；不会输出或请求机场订阅")
    parser.add_argument("--online", action="store_true", help="额外检查公共规则下载地址，不访问节点订阅")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    try:
        config = load(args.config)
        errors = validate(config, root)
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        errors = [f"配置读取失败：{exc}"]
    if not errors and args.online:
        public = [(name, provider) for name, provider in config["rule-providers"].items() if provider["type"] == "http"]
        with ThreadPoolExecutor(max_workers=6) as pool:
            errors.extend(error for error in pool.map(probe, public) if error)
    for error in errors:
        print(f"失败：{error}")
    if not errors:
        print("通过：配置引用和个人规则检查" + ("，公共规则下载检查" if args.online else ""))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
