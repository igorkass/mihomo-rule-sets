import os
import json
import yaml
import requests
import subprocess


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
                for d in rule['domain_suffix']:
                    if d.startswith('.'):
                        # Already has leading dot: .android -> +.android
                        payload.append(f"+{d}")
                    else:
                        # Normal suffix: google.com -> +.google.com
                        payload.append(f"+.{d}")
            if 'domain_keyword' in rule:
                # Keywords are added as-is; mihomo treats them as exact match in binary ruleset
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
        
    yaml_dir = os.path.join(OUTPUT_DIR, "yaml")
    if not os.path.exists(yaml_dir):
        os.makedirs(yaml_dir)

    for url in URLS:
        filename = url.split('/')[-1]
        name_no_ext = os.path.splitext(filename)[0]
        
        # Determine type based on filename
        rule_type = "domain" if "geosite" in filename else "ipcidr"
        
        print(f"Processing {filename} as {rule_type}...")
        
        # 1. Download .srs
        srs_path = f"{name_no_ext}.srs"
        try:
            download_file(url, srs_path)
        except requests.RequestException as e:
            print(f"  Error downloading {filename}: {e}. Skipping.")
            continue
        
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
        
        yaml_filename = f"{name_no_ext}.yaml"
        final_yaml_path = os.path.join(OUTPUT_DIR, "yaml", yaml_filename)
        yaml_data = {"payload": payload}
        
        with open(final_yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f)
            
        # 4. Compile YAML -> .mrs (mihomo)
        mrs_filename = f"{name_no_ext}.mrs"
        output_path = os.path.join(OUTPUT_DIR, mrs_filename)
        
        # mihomo convert-ruleset <type> <input> <output>
        try:
            subprocess.run(["mihomo", "convert-ruleset", rule_type, "yaml", final_yaml_path, output_path], check=True)
            print(f"Successfully converted to {output_path}")
        except FileNotFoundError:
            print("Error: mihomo executable not found.")
            return
        except subprocess.CalledProcessError as e:
             print(f"Error converting {filename}: {e}")

        
        # Cleanup temp files
        if os.path.exists(srs_path): os.remove(srs_path)
        if os.path.exists(json_path): os.remove(json_path)
        # Yaml file kept in releases folder

if __name__ == "__main__":
    main()