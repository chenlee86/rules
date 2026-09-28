import json
import os

SRC_DIR = "rule"
OUT_DIR = "v2rayn/singbox-groups"

os.makedirs(OUT_DIR, exist_ok=True)

skip_prefixes = ("USER-AGENT", "URL-REGEX", "PROCESS-NAME", "AND", "OR", "NOT", "#")

# Clash-style consolidated groups: group name -> (list of source .list files, suggested outbound)
GROUPS = {
    "AI": (
        ["ai.list", "OpenAI.list", "ChatGPT.list", "Claude.list", "Gemini.list",
         "BardAI.list", "Copilot.list", "MetaAI.list", "JetBrainsAI.list",
         "VolcengineAI.list", "Civitai.list"],
        "proxy",
    ),
    "Google": (
        ["Google.list", "GoogleDrive.list", "GoogleEarth.list", "GoogleFCM.list",
         "GoogleSearch.list", "GoogleVoice.list"],
        "proxy",
    ),
    "YouTube": (["YouTube.list", "YouTubeMusic.list"], "proxy"),
    "TikTok": (["TikTok.list"], "proxy"),
    "Telegram": (
        ["Telegram.list", "TelegramNL.list", "TelegramSG.list", "TelegramUS.list"],
        "proxy",
    ),
    "Streaming": (["Netflix.list", "Disney.list", "Spotify.list"], "proxy"),
    "Microsoft": (["Microsoft.list", "MicrosoftEdge.list"], "proxy"),
    "Apple": (
        [f for f in os.listdir(SRC_DIR) if f.startswith("Apple")],
        "proxy",
    ),
    "GitHub": (["GitHub.list"], "proxy"),
    "ChinaDirect": (
        ["China.list", "ChinaMax.list", "ChinaMaxNoIP.list", "ChinaMaxNoMedia.list",
         "ChinaMedia.list", "ChinaNoMedia.list", "ChinaMobile.list", "ChinaTelecom.list",
         "ChinaUnicom.list", "ChinaNews.list", "ChinaIPs.list", "ChinaIPsBGP.list",
         "ChinaDNS.list", "ASN-CN.list", "IPs-CN.list", "AmazonCN.list", "GovCN.list"],
        "direct",
    ),
}


def parse_list_file(path):
    domain, domain_suffix, domain_keyword, ip_cidr = [], [], [], []
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith(skip_prefixes):
                continue
            parts = line.split(",")
            if len(parts) < 2:
                continue
            rule_type = parts[0].strip().upper()
            value = parts[1].strip()
            if not value:
                continue
            if rule_type == "DOMAIN":
                domain.append(value)
            elif rule_type == "DOMAIN-SUFFIX":
                domain_suffix.append(value)
            elif rule_type == "DOMAIN-KEYWORD":
                domain_keyword.append(value)
            elif rule_type in ("IP-CIDR", "IP-CIDR6"):
                ip_cidr.append(value.split(",")[0].strip())
    return domain, domain_suffix, domain_keyword, ip_cidr


manifest = []

for group_name, (files, outbound) in GROUPS.items():
    domain, domain_suffix, domain_keyword, ip_cidr = [], [], [], []
    used_files = []
    for fname in files:
        path = os.path.join(SRC_DIR, fname)
        if not os.path.isfile(path):
            continue
        used_files.append(fname)
        d, ds, dk, ic = parse_list_file(path)
        domain += d
        domain_suffix += ds
        domain_keyword += dk
        ip_cidr += ic

    # de-duplicate while keeping order
    domain = sorted(set(domain))
    domain_suffix = sorted(set(domain_suffix))
    domain_keyword = sorted(set(domain_keyword))
    ip_cidr = sorted(set(ip_cidr))

    rule = {}
    if domain:
        rule["domain"] = domain
    if domain_suffix:
        rule["domain_suffix"] = domain_suffix
    if domain_keyword:
        rule["domain_keyword"] = domain_keyword
    if ip_cidr:
        rule["ip_cidr"] = ip_cidr

    rule_set = {"version": 1, "rules": [rule]}
    out_path = os.path.join(OUT_DIR, f"{group_name}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rule_set, f, ensure_ascii=False, indent=2)

    manifest.append({
        "group": group_name,
        "outbound_suggestion": outbound,
        "source_lists": used_files,
        "domain_count": len(domain) + len(domain_suffix) + len(domain_keyword),
        "ip_count": len(ip_cidr),
    })
    print(f"{group_name}: {len(used_files)} source files -> {out_path}")

with open(os.path.join(OUT_DIR, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
