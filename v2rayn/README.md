# v2rayN 规则

本目录下的规则**基于** [deezertidal/shadowrocket-rules](https://github.com/deezertidal/shadowrocket-rules)（即本仓库 `rule/` 目录下的 Shadowrocket 分流规则）自动转换生成，用于 v2rayN 的自定义路由规则。

## 来源与转换方式

- 原始数据：本仓库 `rule/*.list`（Shadowrocket 格式，`DOMAIN` / `DOMAIN-SUFFIX` / `DOMAIN-KEYWORD` / `IP-CIDR` / `IP-CIDR6` 等规则类型）
- 转换脚本：`convert_v2rayn.py`（仓库根目录）
- 输出目录：`v2rayn/rules/*.json`，每个文件对应一个分流分类（与 `rule/` 下的文件一一对应），格式为 v2ray 标准的路由规则对象（`type: field`），可直接粘贴进 v2rayN 的路由自定义规则 JSON 中，或合并进 `routing.rules` 数组。

字段映射规则：

| Shadowrocket 规则类型 | v2rayN / v2ray 字段 |
| --- | --- |
| `DOMAIN,x` | `domain: ["full:x"]`（精确匹配） |
| `DOMAIN-SUFFIX,x` | `domain: ["domain:x"]`（域名及子域名） |
| `DOMAIN-KEYWORD,x` | `domain: ["x"]`（子串匹配） |
| `IP-CIDR,x` / `IP-CIDR6,x` | `ip: ["x"]` |

以下规则类型无法映射为静态路由规则，转换时会被跳过：`USER-AGENT`、`URL-REGEX`、`PROCESS-NAME`、`GEOIP`、`RULE-SET` 引用、逻辑组合规则（`AND`/`OR`/`NOT`）等。未能提取出任何 `domain`/`ip` 的原始文件名记录在 `v2rayn/skipped_source_lists.txt` 中。

## 使用方法

1. 打开 v2rayN 的路由设置（自定义路由 / Locate Rule）。
2. 从 `v2rayn/rules/` 中选择需要的分类文件（如 `Netflix.json`、`Google.json`），将其内容作为一条 rule 对象加入你的路由配置 `routing.rules` 数组。
3. 按需修改 `outboundTag`（默认写的是 `proxy`，替换成你自己配置里的出站标签名）。

## 同步

`rule/` 目录随上游仓库更新时，重新运行 `python convert_v2rayn.py` 即可重新生成 `v2rayn/rules/` 下的全部文件。
