"""将可编辑的个人规则内嵌到单个远程订阅文件。"""

from pathlib import Path

import yaml

import check


def build(root):
    config = check.load(root / "config.yaml")
    errors = check.validate(config, root)
    if errors:
        raise ValueError("；".join(errors))
    for name, provider in config["rule-providers"].items():
        if provider["type"] == "file":
            config["rule-providers"][name] = {
                "type": "inline",
                "behavior": "classical",
                "payload": check.load(root / provider["path"])["payload"],
            }
    return config


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    config = build(root)
    target = root / "dist" / "config.yaml"
    target.parent.mkdir(exist_ok=True)
    target.write_text("# 自动生成：请修改 config.yaml 或 rule_provider/，不要直接编辑本文件。\n" + yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
    print("已生成 dist/config.yaml：个人规则随主订阅一起更新。")
