export interface NativeSqlProcessor {type:'sql';id:string;name:string;enable:boolean;query:string;parameters:Record<string,string|number|boolean|null>;tables:any[];bindings:{name:string;column:string;row:number}[];maxRows:number;timeoutMs:number;}
export interface NativeScriptHook {type:'script';id:string;name:string;enable:boolean;jobId:string;expectedRevision:number|null;}
export type NativeProcessor = NativeSqlProcessor | NativeScriptHook;
const identifier=/^[A-Za-z_][A-Za-z0-9_]{0,63}$/;
const scalar=(value:unknown)=>value===null||typeof value==='string'||typeof value==='boolean'||(typeof value==='number'&&Number.isFinite(value));
export function readNativeProcessors(raw:string):NativeProcessor[]{
 const data=JSON.parse(raw);if(!Array.isArray(data)||data.length>10)throw Error('每阶段最多10个处理器');
 const ids=new Set<string>();return data.map(item=>{
  if(!item||typeof item!=='object'||Array.isArray(item))throw Error('处理器配置无效');
  if(item.type==='script'){
   const row:NativeScriptHook={type:'script',id:item.id,name:item.name??'脚本钩子',enable:item.enable??true,jobId:item.jobId,expectedRevision:item.expectedRevision??null};
   if(Object.keys(item).some(k=>!['type','id','name','enable','jobId','expectedRevision'].includes(k))||typeof row.id!=='string'||!row.id||row.id.length>36||ids.has(row.id)||typeof row.name!=='string'||row.name.length>255||typeof row.enable!=='boolean'||typeof row.jobId!=='string'||!row.jobId||row.jobId.length>36||(row.expectedRevision!==null&&(!Number.isInteger(row.expectedRevision)||row.expectedRevision<1)))throw Error('脚本钩子引用无效');
   ids.add(row.id);return row;
  }
  if(Object.keys(item).some(k=>!['type','id','name','enable','query','parameters','tables','bindings','maxRows','timeoutMs'].includes(k)))throw Error('处理器配置无效');
  const row={type:item.type??'sql',id:item.id,name:item.name??'只读合成SQL',enable:item.enable??true,query:item.query,parameters:item.parameters??{},tables:item.tables??[],bindings:item.bindings??[],maxRows:item.maxRows??100,timeoutMs:item.timeoutMs??1000};
  if(row.type!=='sql'||typeof row.id!=='string'||!row.id||row.id.length>36||ids.has(row.id)||typeof row.name!=='string'||row.name.length>255||typeof row.enable!=='boolean'||typeof row.query!=='string'||!row.query||row.query.length>8192||!Number.isInteger(row.maxRows)||row.maxRows<1||row.maxRows>1000||!Number.isInteger(row.timeoutMs)||row.timeoutMs<50||row.timeoutMs>2000)throw Error('SQL处理器字段无效');
  ids.add(row.id);
  if(!row.parameters||typeof row.parameters!=='object'||Array.isArray(row.parameters)||Object.entries(row.parameters).length>100||Object.entries(row.parameters).some(([k,v])=>!k||k.length>255||!scalar(v)))throw Error('SQL绑定参数无效');
  if(!Array.isArray(row.tables)||row.tables.length>10||new Set(row.tables.map((t:any)=>String(t.name).toLowerCase())).size!==row.tables.length)throw Error('合成表重复或超限');
  for(const table of row.tables){
   if(!table||typeof table.name!=='string'||!identifier.test(table.name)||!Array.isArray(table.columns)||!table.columns.length||table.columns.length>20||!Array.isArray(table.rows)||table.rows.length>1000||Object.keys(table).some(k=>!['name','columns','rows'].includes(k)))throw Error('合成表无效');
   const names=table.columns.map((c:any)=>c.name);
   if(new Set(names.map((n:any)=>String(n).toLowerCase())).size!==names.length||table.columns.some((c:any)=>!identifier.test(c.name)||!['TEXT','INTEGER','REAL'].includes(c.type??'TEXT')||Object.keys(c).some(k=>!['name','type'].includes(k))))throw Error('合成表列无效');
   if(table.rows.some((r:any)=>!r||typeof r!=='object'||Array.isArray(r)||Object.keys(r).length!==names.length||names.some((n:string)=>!(n in r))||Object.values(r).some(v=>!scalar(v))))throw Error('合成数据行无效');
  }
  if(!Array.isArray(row.bindings)||row.bindings.length>100||new Set(row.bindings.map((b:any)=>b.name)).size!==row.bindings.length||row.bindings.some((b:any)=>!b||typeof b.name!=='string'||!b.name.trim()||b.name.length>255||/[${}\r\n\0]/.test(b.name)||typeof b.column!=='string'||!b.column||b.column.length>255||!Number.isInteger(b.row??0)||(b.row??0)<0||(b.row??0)>999||Object.keys(b).some(k=>!['name','column','row'].includes(k))))throw Error('SQL结果绑定无效');
  if(new TextEncoder().encode(JSON.stringify(row)).length>256*1024)throw Error('SQL配置超过256KiB');
  return row;
 });
}
