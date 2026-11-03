function main(config) {
  const provider = config['proxy-providers']?.['机场订阅'];
  if (!provider || !Array.isArray(config.proxies) || !config.proxies.length) {
    throw new Error('缺少机场订阅模板或有效节点，停止生成手机配置');
  }
  // 节点随主订阅下载，外出时不再依赖家中的 Sub-Store。
  provider.type = 'inline';
  provider.payload = config.proxies;
  for (const key of ['url', 'path', 'interval', 'header']) delete provider[key];
  delete config.proxies;
  config['allow-lan'] = false;
  config['bind-address'] = '127.0.0.1';
  return config;
}
