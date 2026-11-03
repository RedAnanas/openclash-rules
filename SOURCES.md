# 公共规则来源与去向

所有公共规则当前统一来自 MetaCubeX/meta-rules-dat，使用 Mihomo 的 MRS 格式，更新周期 86400 秒。

| 规则集 | 匹配类型 | 策略组 | 上游地址 |
|---|---|---|---|
| 9KG | domain | 9KG | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-porn.mrs) |
| AIChat | domain | 人工智能 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-ai-chat-!cn.mrs) |
| AIChatCN | domain | 全球直连 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-ai-cn.mrs) |
| Apple | domain | 苹果服务 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/apple.mrs) |
| AppleCN | domain | 全球直连 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/apple-cn.mrs) |
| ChinaIP | ipcidr | 全球直连 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/cn.mrs) |
| ChinaSpeedtest | domain | 全球直连 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-speedtest@cn.mrs) |
| Docker | domain | 节点选择 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/docker.mrs) |
| ForeignSpeedtest | domain | 网络测试 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-speedtest.mrs) |
| GameDownload-CN | domain | 全球直连 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-game-platforms-download@cn.mrs) |
| Gemini | domain | 人工智能 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/google-deepmind.mrs) |
| GitHub | domain | 节点选择 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/github.mrs) |
| Google | domain | 谷歌服务 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/google.mrs) |
| Microsoft | domain | 微软服务 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/microsoft.mrs) |
| Microsoft-CN | domain | 全球直连 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/microsoft@cn.mrs) |
| Netflix | domain | Netflix | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/netflix.mrs) |
| NetflixIP | ipcidr | Netflix | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/netflix.mrs) |
| Nintendo | domain | 游戏平台 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/nintendo.mrs) |
| OpenAI | domain | 人工智能 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/openai.mrs) |
| PT | domain | PT站点 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-pt.mrs) |
| PT-!CN | domain | 节点选择 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-pt@!cn.mrs) |
| PT-tracker | domain | PT-tracker | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/tracker.mrs) |
| Private-Domain | domain | DIRECT | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/private.mrs) |
| Private-IP | ipcidr | DIRECT | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/private.mrs) |
| Spotify | domain | Spotify | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/spotify.mrs) |
| Steam | domain | 游戏平台 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/steam.mrs) |
| SteamCN | domain | 全球直连 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/steam@cn.mrs) |
| Telegram | domain | Telegram | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/telegram.mrs) |
| TelegramIP | ipcidr | Telegram | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/telegram.mrs) |
| TikTok | domain | TikTok | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/tiktok.mrs) |
| YouTube | domain | YouTube | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/youtube.mrs) |
| ChinaDomain | domain | 全球直连 | [来源](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/cn.mrs) |

## 维护约定

- config.yaml 中的 rule-providers 是来源的唯一配置位置；本表用于查阅，换源时一并更新。
- 第三方文件由客户端缓存和更新，不手动编辑缓存；个人增补只改 rule_provider/msm-*.yaml。
- 同一分类优先使用一个来源。blackmatrix7 仅作为有明确缺漏时的补充，不整套叠加。
- MetaCubeX 本身整合了部分 blackmatrix7 数据；不同仓库不代表独立来源。
- 404、内容格式错误需要换源；暂时网络错误先检查网络。CDN 不是自动故障转移。
- 换源必须同时核对 format、behavior、文件范围和主规则优先级，保留规则集名称可减少引用改动。
