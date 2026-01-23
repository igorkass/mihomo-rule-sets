# mihomo-rule-sets

## Что это?

Готовые наборы правил для Mihomo и Clash Meta в формате `.mrs`. Это автоматически обновляемая коллекция правил для обхода блокировок и фильтрации рекламы. Правила конвертируются из [runetfreedom/russia-v2ray-rules-dat](https://github.com/runetfreedom/russia-v2ray-rules-dat) (формат sing-box) в формат mihomo. Правила обновляются автоматически каждые 6 часов через GitHub Actions.

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
reject:domain:86400:https://github.com/igorkass/mihomo-rule-sets/raw/release/geosite-category-ads-all.mrs
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
https://github.com/igorkass/mihomo-rule-sets/raw/release/geosite-category-ads-all.mrs
```
