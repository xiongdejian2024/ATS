import type {PlanNode} from '@/api/planTree'

export function categoryNodes(nodes:PlanNode[],category?:PlanNode['category']):PlanNode[]{
  if(!category)return nodes
  const byId=new Map(nodes.map(node=>[node.id,node])),visible=new Set<string>()
  for(const node of nodes.filter(node=>node.category===category)){
    visible.add(node.id)
    let parent=node.parentId;const seen=new Set([node.id])
    while(parent&&!seen.has(parent)){seen.add(parent);const ancestor=byId.get(parent);if(!ancestor||ancestor.nodeType!=='point')break;visible.add(parent);parent=ancestor.parentId}
  }
  return nodes.filter(node=>visible.has(node.id))
}

export interface PlanTreeNode extends PlanNode {children?:PlanTreeNode[]}

export function nodeHierarchy(nodes:PlanNode[]):PlanTreeNode[]{
  const ids=new Set(nodes.map(node=>node.id)),seen=new Set<string>()
  const build=(node:PlanNode):PlanTreeNode=>{seen.add(node.id);const children=nodes.filter(item=>item.parentId===node.id&&!seen.has(item.id)).sort((a,b)=>a.position-b.position).map(build);return {...node,children:children.length?children:undefined}}
  const roots=nodes.filter(node=>!node.parentId||!ids.has(node.parentId)).sort((a,b)=>a.position-b.position).map(build)
  // 仅处理异常旧数据的循环；服务端正常写入仍禁止循环。
  for(const node of nodes)if(!seen.has(node.id))roots.push(build(node))
  return roots
}
