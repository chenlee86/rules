import json
import os
import re

SRC_DIR = "rule"
OUT_DIR = "v2rayn/singbox"

os.makedirs(OUT_DIR, exist_ok=True)

skip_prefixes = ("USER-AGENT", "URL-REGEX", "PROCESS-NAME", "AND", "OR", "NOT", "#")

converted = 0
skipped_files = []

for fname in sorted(os.listdir(SRC_DIR)):
    if not fname.endswith(".list"):
        continue
    domain = []
    domain_suffix = []
    domain_keyword = []
    ip_cidr = []
    with open(os.path.join(SRC_DIR, fname), encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith(skip_prefixes):
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

    if not (domain or domain_suffix or domain_keyword or ip_cidr):
        skipped_files.append(fname)
        continue

    rule = {}
    if domain:
        rule["domain"] = domain
    if domain_suffix:
        rule["domain_suffix"] = domain_suffix
    if domain_keyword:
        rule["domain_keyword"] = domain_keyword
    if ip_cidr:
        rule["ip_cidr"] = ip_cidr

    rule_set = {
        "version": 1,
        "rules": [rule],
    }

    name = fname[:-5]
    out_name = re.sub(r"[^A-Za-z0-9_.-]", "_", name) + ".json"
    with open(os.path.join(OUT_DIR, out_name), "w", encoding="utf-8") as f:
        json.dump(rule_set, f, ensure_ascii=False, indent=2)
    converted += 1

print(f"converted={converted} skipped={len(skipped_files)}")
