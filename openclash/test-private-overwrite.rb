require 'yaml'

root = File.join(ENV.fetch('TMPDIR', '/tmp'), "msm-overwrite-test-#{Process.pid}")
Dir.mkdir(root, 0700)
begin
  private_path = File.join(root, 'private.yaml')
  private_config = {
    'proxy-providers' => { '机场订阅' => { 'type' => 'http', 'url' => 'https://example.invalid/local' } },
    'rules' => ['DOMAIN-SUFFIX,example.test,DIRECT'],
    'dns' => { 'fake-ip-filter' => ['+.example.test'] }
  }
  File.write(private_path, private_config.to_yaml)
  script = File.read(File.join(__dir__, 'msm-private-overwrite.sh'))
  script_path = File.join(root, 'overwrite.sh')
  File.write(script_path, script.gsub('/etc/openclash/custom/msm-private.yaml', private_path))
  File.write(File.join(root, 'uci'), <<~SH)
    #!/bin/sh
    case "$3" in
      openclash.msm_airport.enable) echo 1 ;;
      openclash.msm_airport.param) echo 'MSM_AIRPORT_URL=https://example.invalid/web' ;;
    esac
  SH
  File.chmod(0700, File.join(root, 'uci'))

  %w[msm.yaml yaml_config_tmp_msm.yaml msm-unified.yaml yaml_config_tmp_msm-unified.yaml 组合节点.yaml yaml_config_tmp_组合节点.yaml unrelated.yaml].each do |name|
    provider = { 'type' => 'inline', 'payload' => [{ 'name' => '测试节点', 'type' => 'direct' }] }
    input = {
      'find-process-mode' => false,
      'proxy-providers' => { '机场订阅' => provider },
      'rules' => ['MATCH,DIRECT'], 'dns' => { 'fake-ip-filter' => ['*.lan'] }
    }
    path = File.join(root, name)
    original = input.to_yaml
    File.write(path, original)
    previous = nil
    2.times do
      status = system({ 'PATH' => "#{root}:#{ENV['PATH']}" }, 'sh', script_path, path)
      raise '覆写执行失败' unless status
      output = YAML.load_file(path)
      if name == 'unrelated.yaml'
        raise '无关配置被改动' unless File.read(path) == original
      else
        raise 'off 类型错误' unless output['find-process-mode'] == 'off'
        expected = name.include?('msm-unified') || name.include?('组合节点') ? provider : { 'type' => 'http', 'url' => 'https://example.invalid/web' }
        raise '节点源被错误替换' unless output['proxy-providers']['机场订阅'] == expected
        raise '个人规则未保留' unless output['rules'].include?(private_config['rules'][0])
        raise 'DNS 例外未保留' unless output['dns']['fake-ip-filter'].include?('+.example.test')
      end
      raise '重复覆写改变结果' if previous && output != previous
      previous = output
    end
  end
ensure
  Dir.children(root).each { |name| File.unlink(File.join(root, name)) }
  Dir.rmdir(root)
end
puts '本地覆写检查通过'
