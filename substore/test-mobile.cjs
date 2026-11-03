const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const context = {};
vm.createContext(context);
vm.runInContext(fs.readFileSync(`${__dirname}/mobile.js`, 'utf8'), context);
const nodes = [{ name: '测试日本节点', type: 'direct' }];
const health = { enable: true, interval: 300 };
const groups = [{ name: '日本节点', use: ['机场订阅'], filter: '日本' }];
const result = context.main({
  proxies: nodes,
  'proxy-providers': { 机场订阅: {
    type: 'http', url: 'https://example.invalid/private',
    path: './nodes.yaml', interval: 3600, header: {}, 'health-check': health,
  } },
  'proxy-groups': groups,
});
assert.equal(result['proxy-providers']['机场订阅'].payload, nodes);
assert.equal(result['proxy-providers']['机场订阅']['health-check'], health);
assert.equal(result['proxy-providers']['机场订阅'].type, 'inline');
assert.equal(result['proxy-groups'], groups);
assert.equal(result['allow-lan'], false);
assert.equal(result['bind-address'], '127.0.0.1');
for (const key of ['url', 'path', 'interval', 'header']) {
  assert.equal(key in result['proxy-providers']['机场订阅'], false);
}
assert.equal('proxies' in result, false);
assert.throws(() => context.main({}), /缺少机场订阅模板或有效节点/);
assert.throws(() => context.main({
  proxies: [], 'proxy-providers': { 机场订阅: {} },
}), /缺少机场订阅模板或有效节点/);
console.log('手机配置合成检查通过');
