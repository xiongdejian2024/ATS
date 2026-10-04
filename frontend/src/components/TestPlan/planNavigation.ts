import type { PlanModule } from '@/api/planWorkspace';
import type { PlanGroup } from '@/api/planOrchestration';
export interface NavigationPlan { id:string;name:string;moduleId?:string|null;groupId?:string|null }
export interface PlanNavigationNode {key:string;title:string;kind:'module'|'group'|'plan';id:string;count:number;children:PlanNavigationNode[]}
/** 计划组成员仅出现在组下，模块计数包含所有后代；异常父链也不会生成循环。 */
export function buildPlanNavigation(modules:PlanModule[],groups:PlanGroup[],plans:NavigationPlan[]):PlanNavigationNode[] {
  const roots:PlanNavigationNode[]=[];
  const byModule=new Map(modules.map(m=>[m.id,{key:`module:${m.id}`,id:m.id,title:m.name,kind:'module' as const,count:0,children:[] as PlanNavigationNode[]}]));
  const byGroup=new Map(groups.map(g=>[g.id,{key:`group:${g.id}`,id:g.id,title:g.name,kind:'group' as const,count:0,children:[] as PlanNavigationNode[]}]));
  for(const m of modules){
    const seen=new Set([m.id]);let parent=m.parentId;let cyclic=false;
    while(parent){if(seen.has(parent)){cyclic=true;break}seen.add(parent);parent=modules.find(x=>x.id===parent)?.parentId}
    const target=!cyclic && m.parentId ? byModule.get(m.parentId) : undefined;
    (target?.children || roots).push(byModule.get(m.id)!);
  }
  for(const g of groups)(byModule.get(g.moduleId || '')?.children || roots).push(byGroup.get(g.id)!);
  const seenPlans=new Set<string>();
  for(const p of plans){
    if(seenPlans.has(p.id))continue;seenPlans.add(p.id);
    const group=p.groupId ? byGroup.get(p.groupId) : undefined;
    const target=group || byModule.get(p.moduleId || '');
    (target?.children || roots).push({key:`plan:${p.id}`,id:p.id,title:p.name,kind:'plan',count:1,children:[]});
  }
  function count(node:PlanNavigationNode){if(node.kind!=='plan')node.count=node.children.reduce((sum,child)=>sum+count(child),0);return node.count}
  roots.forEach(count);return roots;
}
export function filterPlanNavigation(nodes:PlanNavigationNode[],keyword:string):PlanNavigationNode[] {
  const query=keyword.trim().toLocaleLowerCase();if(!query)return nodes;
  return nodes.flatMap(node=>{const children=filterPlanNavigation(node.children,query);return node.title.toLocaleLowerCase().includes(query)?[node]:children.length?[{...node,children}]:[]});
}
