#!/bin/sh
# 私密订阅与个人服务例外只在设备本地合并，不上传 GitHub。
case "${1##*/}" in msm.yaml) ;; *) exit 0 ;; esac
ruby -ryaml -e '
  config = YAML.load_file(ARGV[0])
  private = YAML.load_file("/etc/openclash/custom/msm-private.yaml")
  config.fetch("proxy-providers")["机场订阅"] = private.fetch("proxy-providers").fetch("机场订阅")
  config["rules"] = (Array(private["rules"]) + Array(config["rules"])).uniq
  config["dns"]["fake-ip-filter"] = (Array(config["dns"]["fake-ip-filter"]) + Array(private.dig("dns", "fake-ip-filter"))).uniq
  File.write(ARGV[0], config.to_yaml)
' "$1"
