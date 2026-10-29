# Wi-Fi Calling 分流规则

提供可公开下载的纯文本 `.list` 文件，使用 `DOMAIN`、`DOMAIN-SUFFIX` 和 `IP-CIDR`，每行一条，不包含 YAML 的引号、列表前缀或出站节点名。

## 导入链接

| 文件 | 用途 | Raw 链接 |
| --- | --- | --- |
| UK.list | 英国运营商合集 | https://raw.githubusercontent.com/chenlee86/rules/main/WiFiCalling/UK.list |
| CMLink-UK.list | CMlink UK 单独分流 | https://raw.githubusercontent.com/chenlee86/rules/main/WiFiCalling/CMLink-UK.list |
| O2-DE.list | 德国 O2 单独分流 | https://raw.githubusercontent.com/chenlee86/rules/main/WiFiCalling/O2-DE.list |

## 在 open-box 中导入

1. 在目标分流中选中需要承载流量的出站组或节点。
2. 打开“导入规则”，粘贴上面的 Raw 链接。
3. 点击“预览”，核对域名和 IP，再确认导入。本目录每份列表均少于 200 条。
4. CMlink UK 可先使用已验证能建立隧道的英国 IONOS 节点。O2-DE 与英国 O2/Giffgaff 是不同运营商，不要混淆。
5. 导入后核对最终规则顺序，避免同一域名被更靠前的其他规则抢先匹配。

截图中的“导入规则”会把条目复制到当前站点集；远端文件之后的更新不会自动改写这些已导入条目。长期订阅应使用面板“规则集链接”功能，刷新行为以安装版本为准。

## 与 FakeIP、DNS 和端口规则的关系

- 本文件只匹配分流目标，不会自动排除 FakeIP、配置 DNS 重写、配置 IPv6 网关或打开运营商业务。
- 不包含全设备的 UDP 500/4500 强制规则，避免将其他运营商的隧道一并送往同一个出口。
- 只有在手机流量经过 open-box 时，这些规则才能生效。
- 如果仍需对指定 ePDG 排除 FakeIP，应单独配置 DNS；临时固定真实 IP 的 DNS 重写属于对照测试，需留意网关地址变化。
- 分流命中和存在加密隧道，不等于 IMS 注册或通话一定成功；需要在手机上确认 Wi-Fi Calling 标识和实际功能。

## 来源与范围

- 英国合集中的运营商网站域名和较大网段来自用户提供的社区规则片段，原始 GitHub 链接未提供；网段归属与覆盖范围未逐项重新核验，不应视为官方完整清单。
- CMlink 的 `mnc033.mcc234` 域名，以及 `31.94.76.2`、`.5`、`.9`、`.10`，来自本次会话中观察到的公开 ePDG 目标。
- 德国 O2 的域名及三个 /32 目标同样来自本次观察。IP 为历史观察值，运营商可能轮换地址。
- 较大网段和官网域名可能匹配非 Wi-Fi Calling 流量。仅排查 CMlink 时优先导入 CMLink-UK.list。
- 本目录为手工维护，不附加自动更新承诺，也不声明未验证的运营商覆盖率。
