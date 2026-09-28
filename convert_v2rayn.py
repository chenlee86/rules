import json
import os
import re

SRC_DIR = "rule"
OUT_DIR = "v2rayn/rules"

os.makedirs(OUT_DIR, exist_ok=True)

skip_prefixes = ("USER-AGENT", "URL-REGEX", "PROCESS-NAME", "AND", "OR", "NOT", "#")

converted = 0
skipped_files = []

for fname in sorted(os.listdir(SRC_DIR)):
    if not fname.endswith(".list"):
        continue
    domains = []
    ips = []
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
                domains.append(f"full:{value}")
            elif rule_type == "DOMAIN-SUFFIX":
                domains.append(f"domain:{value}")
            elif rule_type == "DOMAIN-KEYWORD":
                domains.append(value)
            elif rule_type in ("IP-CIDR", "IP-CIDR6"):
                ip_val = value.split(",")[0].strip()
                ips.append(ip_val)
            # other types (GEOIP, RULE-SET, FINAL, etc.) are not portable to a
            # static v2ray routing rule object, so they're intentionally skipped.

    if not domains and not ips:
        skipped_files.append(fname)
        continue

    name = fname[:-5]  # strip ".list"
    rule_obj = {
        "type": "field",
        "remarks": name,
        "outboundTag": "proxy",
    }
    if domains:
        rule_obj["domain"] = domains
    if ips:
        rule_obj["ip"] = ips

    out_name = re.sub(r"[^A-Za-z0-9_.-]", "_", name) + ".json"
    with open(os.path.join(OUT_DIR, out_name), "w", encoding="utf-8") as f:
        json.dump(rule_obj, f, ensure_ascii=False, indent=2)
    converted += 1

print(f"converted={converted} skipped={len(skipped_files)}")
with open("v2rayn/skipped_source_lists.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(skipped_files))
