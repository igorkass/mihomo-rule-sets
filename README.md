# mihomo-rule-sets

## Что это?

Готовые наборы правил для Mihomo и Clash Meta в формате `.mrs`. Это автоматически обновляемая коллекция правил для обхода блокировок и фильтрации рекламы. Правила конвертируются из [runetfreedom/russia-v2ray-rules-dat](https://github.com/runetfreedom/russia-v2ray-rules-dat) (формат sing-box) в формат mihomo. Для правил блокировки рекламы используются дополнительные источники из [burjuyz/RuRulesets](https://github.com/burjuyz/RuRulesets). Файлы обновляются автоматически каждые 6 часов.

## Как использовать

Файлы доступны в ветке [release](https://github.com/igorkass/mihomo-rule-sets/tree/release):
- `.mrs` файлы — в корне ветки
- `.yaml` файлы (для просмотра содержимого) — в папке `yaml`

### Для vpnbot

Добавьте в `Routes → Ruleset`:

```
proxy:domain:86400:https://github.com/igorkass/mihomo-rule-sets/raw/release/geosite-ru-blocked.mrs,
proxy:ipcidr:86400:https://github.com/igorkass/mihomo-rule-sets/raw/release/geoip-ru-blocked.mrs,
proxy:domain:86400:https://github.com/igorkass/mihomo-rule-sets/raw/release/geosite-google.mrs,
proxy:ipcidr:86400:https://github.com/igorkass/mihomo-rule-sets/raw/release/geoip-google.mrs,
proxy:domain:86400:https://github.com/igorkass/mihomo-rule-sets/raw/release/geosite-meta.mrs,
proxy:ipcidr:86400:https://github.com/igorkass/mihomo-rule-sets/raw/release/geoip-facebook.mrs,
proxy:domain:86400:https://github.com/igorkass/mihomo-rule-sets/raw/release/geosite-telegram.mrs,
proxy:ipcidr:86400:https://github.com/igorkass/mihomo-rule-sets/raw/release/geoip-telegram.mrs,
reject:domain:86400:https://github.com/igorkass/mihomo-rule-sets/raw/release/ruleset-domain-adaway_alive_hosts_mail_fb.mrs,
reject:domain:86400:https://github.com/igorkass/mihomo-rule-sets/raw/ruleset-domain-oisd_big.mrs
```

### Прямые ссылки

```
https://github.com/igorkass/mihomo-rule-sets/raw/release/geosite-ru-blocked.mrs
https://github.com/igorkass/mihomo-rule-sets/raw/release/geoip-ru-blocked.mrs
https://github.com/igorkass/mihomo-rule-sets/raw/release/geosite-google.mrs
https://github.com/igorkass/mihomo-rule-sets/raw/release/geoip-google.mrs
https://github.com/igorkass/mihomo-rule-sets/raw/release/geosite-meta.mrs
https://github.com/igorkass/mihomo-rule-sets/raw/release/geoip-facebook.mrs
https://github.com/igorkass/mihomo-rule-sets/raw/release/geosite-telegram.mrs
https://github.com/igorkass/mihomo-rule-sets/raw/release/geoip-telegram.mrs
https://github.com/igorkass/mihomo-rule-sets/raw/release/ruleset-domain-adaway_alive_hosts_mail_fb.mrs
https://github.com/igorkass/mihomo-rule-sets/raw/release/ruleset-domain-oisd_big.mrs
```
