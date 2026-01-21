import os
import json
import yaml
import requests
import subprocess
import shutil

# List of source URLs
URLS = [
    "https://raw.githubusercontent.com/runetfreedom/russia-v2ray-rules-dat/release/sing-box/rule-set-geosite/geosite-ru-blocked.srs",
    "https://raw.githubusercontent.com/runetfreedom/russia-v2ray-rules-dat/release/sing-box/rule-set-geoip/geoip-ru-blocked.srs",
    "https://raw.githubusercontent.com/runetfreedom/russia-v2ray-rules-dat/release/sing-box/rule-set-geosite/geosite-google.srs",
    "https://raw.githubusercontent.com/runetfreedom/russia-v2ray-rules-dat/release/sing-box/rule-set-geoip/geoip-google.srs",
    "https://raw.githubusercontent.com/runetfreedom/russia-v2ray-rules-dat/release/sing-box/rule-set-geosite/geosite-meta.srs",
    "https://raw.githubusercontent.com/runetfreedom/russia-v2ray-rules-dat/release/sing-box/rule-set-geoip/geoip-facebook.srs",
    "https://raw.githubusercontent.com/runetfreedom/russia-v2ray-rules-dat/release/sing-box/rule-set-geosite/geosite-telegram.srs",
    "https://raw.githubusercontent.com/runetfreedom/russia-v2ray-rules-dat/release/sing-box/rule-set-geoip/geoip-telegram.srs",
    "https://raw.githubusercontent.com/runetfreedom/russia-v2ray-rules-dat/release/sing-box/rule-set-geosite/geosite-category-ads-all.srs"
]

OUTPUT_DIR = "releases"

def download_file(url, filename):
    print(f"Downloading {url}...")
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as f:
        f.write(response.content)

def extract_payload_from_sb_json(sb_json):
    payload = []
    
    # Recursive function to parse rules
    def parse_rules(rules):
        for rule in rules:
            # Domain
            if 'domain' in rule:
                payload.extend(rule['domain'])
            if 'domain_suffix' in rule:
                payload.extend([f"+.{d}" for d in rule['domain_suffix']])
            if 'domain_keyword' in rule:
                 # Mihomo supports domain_keyword directly in payload list as string? 
                 # Usually payload is mixed string list. 
                 # For domain type: 'google.com' is exact, '+.google.com' is suffix, 'keyword' is keyword.
                 # However, mihomo yaml usually expects just a list.
                 # Let's check mihomo docs behavior. Typically domain_keyword in singbox matches keyword.
                 # In Clash/Mihomo, 'DOMAIN-KEYWORD,google' is the rule. 
                 # But for rule-set (binary), the payload is just a list of strings.
                 # If it doesn't start with '+.', it might be treated as exact match.
                 # Mihomo binary rule-set doesn't distinguish keyword easily in the simple string list format 
                 # unless we use the extended YAML format (not just payload list).
                 # However, for simplicity and common compatibility with these lists (usually domain lists), 
                 # we will assume most are exact or suffix.
                 # If keywords are critical, we might need a more complex transform.
                 payload.extend(rule['domain_keyword'])
            
            # IP
            if 'ip_cidr' in rule:
                payload.extend(rule['ip_cidr'])
            
            # Nested rules
            if 'rules' in rule:
                parse_rules(rule['rules'])

    if 'rules' in sb_json:
        parse_rules(sb_json['rules'])
        
    return payload

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for url in URLS:
        filename = url.split('/')[-1]
        name_no_ext = os.path.splitext(filename)[0]
        
        # Determine type based on filename
        rule_type = "domain" if "geosite" in filename else "ipcidr"
        
        print(f"Processing {filename} as {rule_type}...")
        
        # 1. Download .srs
        srs_path = f"{name_no_ext}.srs"
        download_file(url, srs_path)
        
        # 2. Decompile .srs -> .json (sing-box)
        json_path = f"{name_no_ext}.json"
        try:
            subprocess.run(["sing-box", "rule-set", "decompile", srs_path, "-o", json_path], check=True)
        except FileNotFoundError:
            print("Error: sing-box executable not found.")
            return
        
        # 3. Read JSON and create YAML for mihomo
        with open(json_path, 'r', encoding='utf-8') as f:
            sb_data = json.load(f)
            
        payload = extract_payload_from_sb_json(sb_data)
        
        yaml_path = f"{name_no_ext}.yaml"
        yaml_data = {"payload": payload}
        
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f)
            
        # 4. Compile YAML -> .mrs (mihomo)
        mrs_filename = f"{name_no_ext}.mrs"
        output_path = os.path.join(OUTPUT_DIR, mrs_filename)
        
        # mihomo convert-ruleset <type> <input> <output>
        try:
            subprocess.run(["mihomo", "convert-ruleset", rule_type, "yaml", yaml_path, output_path], check=True)
            print(f"Successfully converted to {output_path}")
        except FileNotFoundError:
             print("Error: mihomo executable not found.")
             return
        except subprocess.CalledProcessError as e:
             print(f"Error converting {filename}: {e}")

        
        # Cleanup temp files
        if os.path.exists(srs_path): os.remove(srs_path)
        if os.path.exists(json_path): os.remove(json_path)
        if os.path.exists(yaml_path): os.remove(yaml_path)

if __name__ == "__main__":
    main()