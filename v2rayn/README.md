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

## sing-box 规则集（v2rayN 的"规则集设置"对话框）

v2rayN 较新版本内置 sing-box 核心，规则集需要用 sing-box 的 rule-set JSON 格式（字段为 `domain` / `domain_suffix` / `domain_keyword` / `ip_cidr`，套在 `{"version":1,"rules":[...]}` 里），与上面 `v2rayn/rules/` 下的 v2ray 经典 `routing.rules` 格式**不通用**。

对应的 sing-box 格式文件在 [`v2rayn/singbox/`](./singbox)，同样由 `convert_singbox.py` 从 `rule/*.list` 自动生成。

### 导入方法

打开 v2rayN 的「规则集设置」窗口：

- **方式一：填自定义 sing-box rule-set 的 URL**（推荐，能跟着仓库更新）
  在"自定义 sing-box rule-set"框里填入对应分类文件的 raw 链接，例如：
  `https://raw.githubusercontent.com/chenlee86/rules/main/v2rayn/singbox/Netflix.json`
  再填"别名"，点"确定"。
- **方式二：从文件中导入规则**
  先把 `v2rayn/singbox/xxx.json` 下载到本地，再在对话框顶部点"从文件中导入规则"选择该文件。
- **方式三：从剪贴板中导入规则**
  打开对应 json 文件复制全部内容，点"从剪贴板中导入规则"粘贴。
- **方式四：从订阅 Url 中导入规则**
  同方式一，用于批量订阅场景。

三种格式二选一即可：只用 sing-box 核心就用 `singbox/`，走经典 v2ray 核心路由规则就用 `rules/`。
