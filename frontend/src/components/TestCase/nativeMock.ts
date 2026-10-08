export interface NativeMockResponse { enable: boolean; statusCode: number; headers: Record<string,string>; body: string; delayMs: number; }
export function readMockResponse(raw:string):NativeMockResponse {
  const data=JSON.parse(raw);
  if(!data||typeof data!=='object'||Array.isArray(data)||Object.keys(data).some(k=>!['enable','statusCode','headers','body','delayMs'].includes(k)))throw Error('Mock配置无效');
  const value={enable:data.enable??false,statusCode:data.statusCode??200,headers:data.headers??{},body:data.body??'',delayMs:data.delayMs??0};
  if(typeof value.enable!=='boolean'||!Number.isInteger(value.statusCode)||value.statusCode<200||value.statusCode>599||!Number.isInteger(value.delayMs)||value.delayMs<0||value.delayMs>3000||typeof value.body!=='string'||value.body.length>131072||!value.headers||typeof value.headers!=='object'||Array.isArray(value.headers)||Object.entries(value.headers).length>100||Object.entries(value.headers).some(([k,v])=>!k||k.length>255||typeof v!=='string'||v.length>20000||/[\r\n]/.test(k+v))||new TextEncoder().encode(JSON.stringify(value)).length>256*1024)throw Error('Mock配置超过限制');
  return value;
}
