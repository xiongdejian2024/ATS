import {beforeEach,describe,it,expect,vi} from 'vitest'
const mocks=vi.hoisted(()=>({members:vi.fn()}))
vi.mock('@/api/mentions',()=>({mentionsApi:mocks}))
vi.mock('@/stores/user',()=>({useUserStore:()=>({user:{id:'actor'}})}))
import MentionMemberPicker from './MentionMemberPicker.vue'
import {componentHost,flushComponent as flush} from '@/test/componentHost'
beforeEach(()=>{vi.clearAllMocks();mocks.members.mockResolvedValue({items:[{id:'a',label:'A',username:'a'}],total:1})})
describe('提及成员分页与上下文隔离',()=>{
  it('读取失败可以重试，返回稳定标识与显示名',async()=>{mocks.members.mockRejectedValueOnce(new Error('synthetic'));const {state:s,stop}=componentHost(MentionMemberPicker,{projectId:'p',context:'case'});const result=s.pick();await flush();expect(s.error).toBeTruthy();s.searchMembers();await flush();s.choose(s.members[0]);expect(await result).toEqual({id:'a',label:'A',username:'a'});stop()})
  it('切项目终止旧选择，迟到响应不能覆盖新成员',async()=>{let finish!:(v:any)=>void;mocks.members.mockReturnValueOnce(new Promise(r=>finish=r));const {state:s,props,stop}=componentHost(MentionMemberPicker,{projectId:'old',context:'case'});const old=s.pick();props.projectId='new';await flush();expect(await old).toBeUndefined();const latest=s.pick();await flush();finish({items:[{id:'old',label:'Old'}],total:1});await flush();expect(s.members[0].id).toBe('a');s.cancel();expect(await latest).toBeUndefined();stop()})
  it('按20条分页查询，卸载取消未完成选择',async()=>{const {state:s,stop}=componentHost(MentionMemberPicker,{projectId:'p',context:'plan'});const result=s.pick();await flush();s.paginate(2);await flush();expect(mocks.members).toHaveBeenLastCalledWith('p',{context:'plan',search:'',page:2});stop();expect(await result).toBeUndefined();stop()})
})
