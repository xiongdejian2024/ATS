import { it, expect, vi } from 'vitest';
import { reactive, effectScope } from 'vue';
import { readMockResponse } from '../nativeMock';
import { useNativeExecutionDraft } from '../nativeExecutionDraft';
import { phaseTimings, type HttpAttempt } from '@/api/nativeHttpReport';
it('static mock preserves literal body and strictly bounds config',()=>{
 expect(readMockResponse('{"enable":true,"body":"<b>literal</b>"}').body).toBe('<b>literal</b>');
 for(const value of [{enable:1},{statusCode:599.5},{delayMs:3001},{headers:{x:'a\r\nb'}},{body:'中'.repeat(131072)}])expect(()=>readMockResponse(JSON.stringify(value))).toThrow();
});
it('unfinished mock draft cannot overwrite valid execution JSON',()=>{
 const props=reactive({category:'api',modelValue:'{"request":{}}',apiCases:[]});const scope=effectScope();const errors:string[]=[];
 const spy=vi.spyOn(console,'error').mockImplementation(()=>{});
 try{const state=scope.run(()=>useNativeExecutionDraft(props,{update:v=>props.modelValue=v,error:v=>errors.push(v),draft:()=>{}}))!;
 state.mockResponse.value='{"enable":true,"body":"frozen"}';state.reportPhases.value=true;const saved=props.modelValue;
 state.mockResponse.value='{';expect(props.modelValue).toBe(saved);expect(errors.at(-1)).toBeTruthy();
 props.modelValue='{}';props.modelValue=saved;expect(readMockResponse(state.mockResponse.value).body).toBe('frozen');
 }finally{scope.stop();spy.mockRestore();}
});
it('historical missing timing is explicit and Mock phase is identified',()=>{
 const rows=phaseTimings({source:'mock',timings:{httpMs:12}} as HttpAttempt);
 expect(rows[1]).toMatchObject({name:'Mock响应',value:'12.000 ms'});expect(rows[0].value).toBe('未记录');
});
