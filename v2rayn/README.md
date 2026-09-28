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

## 分组合并规则集（类似 Clash 的 Rule Provider，推荐日常使用）

逐个分类导入太麻烦，[`v2rayn/singbox-groups/`](./singbox-groups) 把常用分类合并成了 10 个大类，一个分类只需导入一次：

| 分组文件 | 合并的原始规则 | 建议出站 |
| --- | --- | --- |
| `AI.json` | ai / OpenAI / ChatGPT / Claude / Gemini / BardAI / Copilot / MetaAI / JetBrainsAI / VolcengineAI / Civitai | proxy |
| `Google.json` | Google / GoogleDrive / GoogleEarth / GoogleFCM / GoogleSearch / GoogleVoice | proxy |
| `YouTube.json` | YouTube / YouTubeMusic | proxy |
| `TikTok.json` | TikTok | proxy |
| `Telegram.json` | Telegram / TelegramNL / TelegramSG / TelegramUS | proxy |
| `Streaming.json` | Netflix / Disney / Spotify | proxy |
| `Microsoft.json` | Microsoft / MicrosoftEdge | proxy |
| `Apple.json` | 所有 Apple* 分类 | proxy |
| `GitHub.json` | GitHub | proxy |
| `ChinaDirect.json` | China / ChinaMax 系列 / ChinaMobile / ChinaTelecom / ChinaUnicom / ChinaNews / ChinaIPs 系列 / ASN-CN / IPs-CN / AmazonCN / GovCN | **direct** |

由 `convert_singbox_groups.py` 从 `rule/*.list` 自动合并生成，每个分组已去重；[`manifest.json`](./singbox-groups/manifest.json) 记录了每个分组包含哪些原始文件及条目数，方便核对或自行调整分组。

### 导入方法

在「规则集设置」窗口，对每个分组重复一次（一共只需 10 次，而不是 766 次）：

1. 「别名」填分组名，比如 `AI`
2. 「自定义 sing-box rule-set」填对应链接：
   `https://raw.githubusercontent.com/chenlee86/rules/main/v2rayn/singbox-groups/AI.json`
3. 点「确定」保存

保存完规则集后，还需要在 v2rayN 的**路由规则**里为每个规则集绑定出站（`AI`/`Google`/`YouTube`/`TikTok`/`Telegram`/`Streaming`/`Microsoft`/`Apple`/`GitHub` 这 9 个走 `proxy`，`ChinaDirect` 走 `direct`），否则规则集只是被导入，不会生效。

### 自定义分组

想调整分组（比如把 Apple 也改成 direct，或者把某个网站单独拆出来），改 `convert_singbox_groups.py` 顶部的 `GROUPS` 字典重新运行即可，源数据始终来自 `rule/*.list`。

## 完整路由规则 JSON（v2rayN 路由设置里直接整体粘贴/导入）

[`v2rayn/routing-rules.json`](./routing-rules.json) 是一份可以直接整体导入 v2rayN「路由设置」的规则数组（基于 geosite/geoip，不依赖本仓库其他自定义规则集），按顺序命中：

1. UDP 443 阻断（防止 QUIC 绕过代理）
2. 局域网直连
3. 广告域名阻断
4. AI 服务走代理
5. YouTube 走代理
6. 国内 IP/域名直连
7. 其余全部走代理

获取方式：
- 直接复制 [`v2rayn/routing-rules.json`](https://raw.githubusercontent.com/chenlee86/rules/main/v2rayn/routing-rules.json) 内容，粘贴进 v2rayN 路由设置的规则列表（支持整体导入 JSON 数组）
- 或在路由设置里用「从 Url 导入」，直接填上面的 raw 链接
