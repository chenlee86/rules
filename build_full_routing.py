import json
import os

GROUPS_DIR = "v2rayn/singbox-groups"
OUT_PATH = "v2rayn/routing-rules-full.json"

GROUP_ORDER = [
    ("AI", "AI专用规则"),
    ("Google", "Google全家桶"),
    ("YouTube", "油管专用规则"),
    ("TikTok", "TikTok专用规则"),
    ("Telegram", "Telegram专用规则"),
    ("Streaming", "流媒体(Netflix/Disney+/Spotify)"),
    ("Microsoft", "Microsoft/Edge专用规则"),
    ("Apple", "Apple服务专用规则"),
    ("GitHub", "GitHub专用规则"),
]


def load_group_as_v2ray_rule(group_name, remarks, outbound="proxy"):
    path = os.path.join(GROUPS_DIR, f"{group_name}.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    rule = data["rules"][0]

    domain = []
    for d in rule.get("domain", []):
        domain.append(f"full:{d}")
    for d in rule.get("domain_suffix", []):
        domain.append(f"domain:{d}")
    for d in rule.get("domain_keyword", []):
        domain.append(d)
    ip = rule.get("ip_cidr", [])

    obj = {
        "type": "field",
        "outboundTag": outbound,
        "enabled": True,
        "remarks": remarks,
    }
    if domain:
        obj["domain"] = domain
    if ip:
        obj["ip"] = ip
    return obj


rules = []

rules.append({
    "port": "443",
    "network": "udp",
    "outboundTag": "block",
    "enabled": True,
    "remarks": "UDP443阻断",
})

rules.append({
    "outboundTag": "direct",
    "ip": ["geoip:private"],
    "domain": ["geosite:private"],
    "enabled": True,
    "remarks": "局域网专用规则",
})

rules.append({
    "outboundTag": "block",
    "domain": ["geosite:category-ads-all"],
    "enabled": True,
    "remarks": "广告拦截",
})

for group_name, remarks in GROUP_ORDER:
    rules.append(load_group_as_v2ray_rule(group_name, remarks))

rules.append({
    "outboundTag": "direct",
    "ip": ["geoip:cn"],
    "domain": ["geosite:cn"],
    "enabled": True,
    "remarks": "国内直连",
})

rules.append({
    "port": "0-65535",
    "outboundTag": "proxy",
    "enabled": True,
    "remarks": "国外代理",
})

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(rules, f, ensure_ascii=False, indent=2)

print(f"wrote {len(rules)} rules to {OUT_PATH}")
