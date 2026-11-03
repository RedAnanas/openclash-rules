#!/bin/sh
# 私密订阅与个人服务例外只在设备本地合并，不上传 GitHub。
case "${1##*/}" in msm.yaml|yaml_config_tmp_msm.yaml) ;; *) exit 0 ;; esac
ruby -ryaml -e '
  config = YAML.load_file(ARGV[0])
  private = YAML.load_file("/etc/openclash/custom/msm-private.yaml")
  airport_url = ENV["MSM_AIRPORT_URL"]
  if IO.popen(["uci", "-q", "get", "openclash.msm_airport.enable"], &:read).strip == "1"
    param = IO.popen(["uci", "-q", "get", "openclash.msm_airport.param"], &:read)
    entry = param.split(";").find { |item| item.strip.start_with?("MSM_AIRPORT_URL=") }
    airport_url = entry.strip.split("=", 2)[1] if entry
  end
  if airport_url && !airport_url.empty?
    raise "机场订阅地址必须是 HTTP 或 HTTPS 链接" unless airport_url.match?(/\Ahttps?:\/\/\S+\z/)
    private.fetch("proxy-providers").fetch("机场订阅")["url"] = airport_url
  end
  config.fetch("proxy-providers")["机场订阅"] = private.fetch("proxy-providers").fetch("机场订阅")
  config["rules"] = (Array(private["rules"]) + Array(config["rules"])).uniq
  config["dns"]["fake-ip-filter"] = (Array(config["dns"]["fake-ip-filter"]) + Array(private.dig("dns", "fake-ip-filter"))).uniq
  File.write(ARGV[0], config.to_yaml)
' "$1"
