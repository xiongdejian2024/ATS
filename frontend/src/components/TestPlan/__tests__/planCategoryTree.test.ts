import {describe,expect,it} from 'vitest'
import {categoryNodes,nodeHierarchy} from '../planCategoryTree'
import type {PlanNode} from '@/api/planTree'
const node=(id:string,parentId:string|null,category:PlanNode['category']='functional',nodeType:PlanNode['nodeType']='case',position=0):PlanNode=>({id,parentId,category,nodeType,position,name:id,planId:'plan',config:{},effectiveConfig:{}})
describe('计划分类树隔离',()=>{
  it('保留测试点祖先，排除同级其他分类和无关子树',()=>{
    const nodes=[node('root',null,'functional','point'),node('point','root','functional','point'),node('api','point','api'),node('manual','point'),node('other',null)]
    const filtered=categoryNodes(nodes,'api')
    expect(filtered.map(row=>row.id)).toEqual(['root','point','api'])
    expect(nodeHierarchy(filtered)[0].children?.[0].children?.map(row=>row.id)).toEqual(['api'])
    expect(categoryNodes(nodes)).toBe(nodes)
  })
  it('孤立节点和循环旧数据不丢失且不无限递归',()=>{
    const nodes=[node('a','b','api','point'),node('b','a','functional','point'),node('orphan','missing','api'),node('later',null,'api','case',2),node('first',null,'api','case',1)]
    const filtered=categoryNodes(nodes,'api'),tree=nodeHierarchy(filtered)
    const flattened:string[]=[];const visit=(rows:any[])=>rows.forEach(row=>{flattened.push(row.id);if(row.children)visit(row.children)})
    visit(tree)
    expect(new Set(flattened)).toEqual(new Set(nodes.map(row=>row.id)))
    expect(flattened.length).toBe(nodes.length)
    expect(tree.findIndex(row=>row.id==='first')).toBeLessThan(tree.findIndex(row=>row.id==='later'))
  })
})
