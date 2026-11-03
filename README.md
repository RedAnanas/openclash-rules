# OpenClash 远程分流配置

一份支持 Mihomo／Meta 内核的 OpenClash 配置。包含 31 个策略组、32 个第三方规则集和 6 类自定义规则；真实机场订阅与私密服务例外保留在设备本地。

远程订阅地址：

```text
https://raw.githubusercontent.com/RedAnanas/openclash-rules/main/dist/config.yaml
```

## 日常更新

1. 修改下表对应文件，在 GitHub 提交或上传到 main 分支。
2. 等待仓库 Actions 中“校验并生成远程订阅”成功。工作流会自动更新 dist/config.yaml。
3. 在 OpenClash 更新名为 msm 的配置订阅，更新后重载生效。无需再逐个上传个人规则文件。

| 需求 | 修改位置 |
|---|---|
| 强制直连 | rule_provider/msm-direct.yaml |
| 强制进入节点选择 | rule_provider/msm-proxy.yaml |
| 屏蔽域名 | rule_provider/msm-reject.yaml |
| AI 漏收录补充 | rule_provider/msm-ai.yaml |
| PT 站点补充 | rule_provider/msm-pt.yaml |
| 固定香港出口 | rule_provider/msm-hongkong.yaml |
| 策略组、XS 地区筛选、测速周期 | config.yaml 的 proxy-groups |
| 第三方来源、更新周期 | config.yaml 的 rule-providers |
| 分流优先级 | config.yaml 的 rules |

自定义规则只写匹配条件，不填写出口：

```yaml
payload:
  # 补充上游未收录的服务
  - DOMAIN-SUFFIX,example.com
```

删除最后一条时保留 payload: []。规则从上往下匹配，个人屏蔽、直连、代理和服务例外优先于第三方分类。

## 为什么更新一个链接就够

config.yaml 和 rule_provider/ 是编辑源文件。build.py 将 6 类自定义规则转成 inline 提供者，打包进 dist/config.yaml，因此主订阅更新时这些规则一并更新，不受外部规则缓存周期影响。不要直接编辑 dist/config.yaml，它会被自动生成覆盖。

32 个第三方规则集仍独立从 MetaCubeX 下载，默认每天更新。主订阅控制它们的来源与分流去向，第三方域名内容由对应上游维护。

## OpenClash 首次接入

当前维护者的设备已配置。新设备只需进行一次本地私密设置：

1. 从 openclash/private.example.yaml 复制一份到设备 /etc/openclash/custom/msm-private.yaml，填写真实机场订阅；需要保留的私密域名可写入该文件的 rules 与 dns.fake-ip-filter。
2. 将 openclash/msm-private-overwrite.sh 上传到设备 /etc/openclash/custom/msm-private-overwrite.sh，赋予执行权限。私密配置权限设为 600。
3. 在设备现有 /etc/openclash/custom/openclash_custom_overwrite.sh 的 exit 0 之前添加：

   ```sh
   /etc/openclash/custom/msm-private-overwrite.sh "$CONFIG_FILE" || exit 1
   ```

4. 在 OpenClash 的“配置订阅”新增订阅，配置名填写 msm，地址使用上面的远程链接，关闭在线订阅转换；下载后选择 msm.yaml。
5. 使用 Mihomo／Meta 内核，保留符合设备网络的 DNS、IPv6 与接管设置；检查插件覆写是否会再次替换规则或策略组。需要个人强制代理规则生效时，应关闭大陆 IP 绕过。
6. 首次加载检查日志、节点数量与目标网站的命中规则。

本地覆写只对 msm.yaml 生效，每次重载都会重新注入私密订阅和个人服务例外。更换机场时只修改设备的 msm-private.yaml，不修改 GitHub。需要公开同步的通用例外写入仓库；仅供自己使用的例外放在设备本地。

当前私密覆写为 OpenClash 提供。其他 Mihomo 客户端需要使用其本地合并功能注入机场订阅，不能仅导入占位模板就使用节点。

## 在网页更换机场

已有设备可配置本地模块 `openclash/msm-airport.conf`，参数仍仅保存在设备上。维护者当前设备已经配置好。

1. 打开 OpenClash → 运行状态 → 覆写模块。
2. 在底部找到 `msm-airport.conf`，点击其齿轮“编辑模块信息”。
3. 在“环境变量”中保留 `MSM_AIRPORT_URL=`，只替换等号后面的机场订阅链接。
4. 保存，关闭编辑窗口，重启 OpenClash。链接应返回 Clash／Mihomo 格式的节点。

该模块保持启用，只作用于 msm.yaml。脚本直接读取网页保存的参数，优先于私密文件中的旧地址。GitHub 主订阅保持不变；不要把真实参数写入仓库。新设备使用该入口时，需将模块上传为本地覆写模块并选择 msm.yaml，按需填写参数并启用。

这套方式由 Mihomo 直接读取节点。订阅转换器“机场链接＋规则模板”也是可选方案，但需要匹配的转换模板和可用的转换后端；当前 GitHub 主 YAML 不能直接作为 subconverter 的外部 INI 模板。

## 自动与手动分组

地区组、高级、省流、游戏、自动选择，以及 XS 日本自动和 XS 美国自动使用 url-test。XS 两组仅筛选对应地区且以 XS 开头的节点，每 300 秒测速，容差 50 毫秒。

人工智能等服务组为 select：手动选定地区或专属组后，由其下级自动组选择具体节点。空组的 COMPATIBLE 是占位，不是实际节点。

## 本地校验

需要 Python 3.10+ 和 PyYAML：

```sh
python -m pip install -r requirements.txt
python check.py
python -m unittest -v
python build.py
python check.py --config dist/config.yaml
```

check.py --online 可额外检查第三方下载地址，但不请求机场订阅。加载配置仍需用实际 Mihomo 内核验证，自动检查不能证明所有服务均可访问或解锁。

## 分享与回退

不要提交真实机场 URL、节点密码、管理密钥或私密服务域名。config.local.yaml、config.private.yaml、缓存、设备备份和本地部署记录均被 Git 忽略。

GitHub 历史可回退编辑源文件，回退后重新运行生成工作流，再更新客户端订阅。设备首次接入前应备份原主配置、OpenClash 设置和覆写脚本。

参考：[MetaCubeX 规则库](https://github.com/MetaCubeX/meta-rules-dat)、[Mihomo 规则提供者](https://wiki.metacubex.one/config/rule-providers/)。
