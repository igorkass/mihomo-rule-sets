# mihomo-rule-sets

Этот репозиторий содержит автоматически обновляемые и конвертированные наборы правил (rulesets) для Mihomo/Clash Meta.

Исходные данные берутся из репозитория [runetfreedom/russia-v2ray-rules-dat](https://github.com/runetfreedom/russia-v2ray-rules-dat/tree/release/sing-box) и конвертируются из формата `srs` (sing-box) в `mrs` (mihomo/clash binary).

Готовые файлы публикуются в ветку [release](https://github.com/igorkass/mihomo-rule-sets/tree/release).

*   Бинарные файлы `.mrs` находятся в корне ветки `release`.
*   YAML файлы для просмотра находятся в папке `yaml` ветки `release`.

## Список правил

Вы можете скопировать следующий блок в конфигурацию `Vless -> routes -> rulesset list`:

```yaml
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

## Автоматическое обновление

Обновление происходит ежедневно в 04:00 UTC с помощью GitHub Actions.