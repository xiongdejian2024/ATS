import {describe,expect,it} from 'vitest';
import {buildPlanNavigation,filterPlanNavigation} from '../planNavigation';
describe('计划模块、组与成员的导航一致性',()=>{
  it('成员只出现一次，父模块计数包含后代及组内计划，搜索保留父链',()=>{
    const modules=[{id:'root',name:'发布',position:0},{id:'child',name:'回归',parentId:'root',position:0}];
    const groups=[{id:'g',name:'执行组',moduleId:'child',planCount:1}];
    const plans=[{id:'a',name:'文本验收',moduleId:'root',groupId:'g'},{id:'b',name:'接口验收',moduleId:'child'},{id:'b',name:'接口验收',moduleId:'child'}];
    const tree=buildPlanNavigation(modules,groups,plans);
    expect(tree[0].count).toBe(2);
    expect(tree[0].children[0].count).toBe(2);
    expect(tree[0].children[0].children[0].children[0].id).toBe('a');
    const filtered=filterPlanNavigation(tree,'文本');
    expect(filtered[0].children[0].children[0].children[0].title).toBe('文本验收');
    expect(filterPlanNavigation(tree,'没有')).toEqual([]);
  });
  it('错误模块父链不形成循环，未分组计划保留在根部',()=>{
    const tree=buildPlanNavigation([{id:'x',name:'甲',parentId:'y',position:0},{id:'y',name:'乙',parentId:'x',position:1}],[],[{id:'p',name:'根计划'}]);
    expect(tree.map(n=>n.id)).toEqual(['x','y','p']);
    expect(tree.map(n=>n.count)).toEqual([0,0,1]);
  });
});
