import {createRouter,createMemoryHistory} from 'vue-router'
import {beforeEach,describe,it,expect,vi} from 'vitest'
const api=vi.hoisted(()=>({source:vi.fn(),markAsRead:vi.fn()}))
vi.mock('@/api/notification',()=>({notificationApi:api}))
import {openNotification} from './notificationNavigation'
import type {Notification} from '@/types'
const item={id:'notice',type:'mention_case_comment'} as Notification
function router(){return createRouter({history:createMemoryHistory(),routes:[{path:'/edit',component:{}},{path:'/mentions/:notificationId',name:'MentionSource',component:{}}]})}
beforeEach(()=>{vi.clearAllMocks();api.source.mockResolvedValue({content:'frozen'});api.markAsRead.mockResolvedValue(undefined)})
describe('通知与真实内存路由守卫',()=>{
  it('草稿守卫拒绝导航时保持未读',async()=>{const r=router();await r.push('/edit');r.beforeEach(()=>false);expect(await openNotification(item,r)).toBe(false);expect(r.currentRoute.value.path).toBe('/edit');expect(api.markAsRead).not.toHaveBeenCalled()})
  it('成功打开来源及重复点击已打开来源都会标记已读',async()=>{const r=router();await r.push('/edit');expect(await openNotification(item,r)).toBe(true);expect(r.currentRoute.value.params.notificationId).toBe('notice');expect(await openNotification(item,r)).toBe(true);expect(api.markAsRead).toHaveBeenCalledTimes(2)})
  it('来源访问被撤销时不导航、不标记已读',async()=>{const r=router();await r.push('/edit');api.source.mockRejectedValueOnce(new Error('revoked'));await expect(openNotification(item,r)).rejects.toThrow('revoked');expect(r.currentRoute.value.path).toBe('/edit');expect(api.markAsRead).not.toHaveBeenCalled()})
})
