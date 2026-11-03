"""验证检查工具能阻止会导致分流配置失效的常见修改。"""

import copy
from pathlib import Path
import re
import tempfile
import unittest

import check
import build


class ConfigChecks(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parent
        self.config = check.load(self.root / "config.yaml")

    def test_配置包引用完整(self):
        self.assertEqual(check.validate(self.config, self.root), [])

    def test_删除仍被引用的规则集会失败(self):
        self.config["rule-providers"].pop("OpenAI")
        self.assertTrue(any("不存在的规则集 OpenAI" in e for e in check.validate(self.config, self.root)))

    def test_策略组改名未同步引用会失败(self):
        self.config["proxy-groups"][0]["name"] = "重命名后"
        self.assertTrue(any("不存在的出口 节点选择" in e for e in check.validate(self.config, self.root)))

    def test_循环引用会失败(self):
        self.config["proxy-groups"][0]["proxies"] = ["节点选择"]
        self.assertTrue(any("循环引用" in e for e in check.validate(self.config, self.root)))

    def test_个人规则不能携带出口(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "invalid.yaml").write_text("payload:\n  - DOMAIN-SUFFIX,example.com,DIRECT\n", encoding="utf-8")
            config = copy.deepcopy(self.config)
            for provider in config["rule-providers"].values():
                if provider["type"] == "file":
                    provider["path"] = "invalid.yaml"
            self.assertTrue(any("不写出口" in e for e in check.validate(config, root)))

    def test_重复字段不能静默覆盖(self):
        with self.assertRaisesRegex(ValueError, "字段重复"):
            check.yaml.load("rules: []\nrules: []\n", Loader=check.UniqueLoader)

    def test_拒绝会被插件重写的自定义目录(self):
        self.config["rule-providers"]["个人直连"]["path"] = "./custom/direct.yaml"
        self.assertTrue(any("原生规则目录" in e for e in check.validate(self.config, self.root)))

    def test_XS自动组只包含对应地区的XS节点(self):
        groups = {group["name"]: group for group in self.config["proxy-groups"]}
        for region, other in [("日本", "美国"), ("美国", "日本")]:
            name = f"XS {region}自动"
            group = groups[name]
            self.assertEqual(group["type"], "url-test")
            self.assertIn(name, groups["人工智能"]["proxies"])
            self.assertRegex(f"XS {region} 家宽 01", group["filter"])
            for wrong in [f"一元 {region} 01", f"良心云 {region} 01", f"XSS {region} 01", f"XS {other} 01"]:
                self.assertIsNone(re.search(group["filter"], wrong))

    def test_远程配置包含全部个人规则且不依赖外部个人文件(self):
        result = build.build(self.root)
        for name, provider in self.config["rule-providers"].items():
            if provider["type"] == "file":
                self.assertEqual(result["rule-providers"][name]["type"], "inline")
                self.assertEqual(result["rule-providers"][name]["payload"], check.load(self.root / provider["path"])["payload"])
        self.assertEqual(check.validate(result, self.root), [])

    def test_公开模板只保留订阅占位且无节点或管理凭据(self):
        for provider in self.config["proxy-providers"].values():
            self.assertEqual(provider["url"], "https://example.invalid/replace-with-your-subscription")
            self.assertEqual(set(provider.get("header", {})), {"User-Agent"})
        for field in ["secret", "authentication", "listeners", "proxies"]:
            self.assertNotIn(field, self.config)


if __name__ == "__main__":
    unittest.main()
