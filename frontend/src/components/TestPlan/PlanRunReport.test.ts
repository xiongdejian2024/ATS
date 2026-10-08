import { createRenderer, nextTick, ssrContextKey } from 'vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
const mocks = vi.hoisted(() => ({ report: vi.fn(), result: vi.fn(), comment: vi.fn(), collaboration: vi.fn(), issues: vi.fn(), confirm: vi.fn(), summary: vi.fn(), shares: vi.fn(), warning: vi.fn(),attachment:vi.fn(),saveIssue:vi.fn(),share:vi.fn(),revoke:vi.fn() }))
vi.mock('ant-design-vue', () => ({ message: { warning: mocks.warning, error: vi.fn(), success: vi.fn() }, Modal: { confirm: mocks.confirm } }))
vi.mock('vue-router', () => ({ onBeforeRouteLeave: vi.fn(), onBeforeRouteUpdate: vi.fn() }))
vi.mock('@/stores/user',()=>({useUserStore:()=>({user:{id:'user'}})}))
vi.mock('./ReportDetailCards.vue',()=>({default:{render:()=>null}}))
vi.mock('@/api/planCollaboration', () => ({ planCollaborationApi: mocks, downloadPlanFile: vi.fn() }))
vi.mock('@/api/caseFeatures', () => ({ caseFeaturesApi: { issues: mocks.issues,saveIssue:mocks.saveIssue } }))
vi.mock('@/api/nativeHttpReport', () => ({ nativeHttpReportApi: { detail: vi.fn() } }))
vi.mock('@/components/TestCase/CaseMindMap.vue', () => ({ default: { render: () => null } }))
vi.mock('@/components/TestCase/CaseRichText.vue', () => ({ default: { render: () => null } }))
vi.mock('@/components/Report/NativeHttpReport.vue', () => ({ default: { render: () => null } }))
import PlanRunReport from './PlanRunReport.vue'
const renderer = createRenderer<any, any>({
  createElement: () => ({ children: [] }), createText: () => ({}), createComment: () => ({}),
  insert(child, parent) { parent.children?.push(child); child.parent = parent },
  remove() {}, setText() {}, setElementText() {}, patchProp() {},
  parentNode: node => node.parent, nextSibling: () => null,
})
const row = { caseId: 'master', associationId: 'copy', caseName: 'frozen', result: 'pending', category: 'functional', snapshot: { steps: [{ action: 'a', expected: 'b' }] } }
const report = () => ({ id: 'run', status: 'running', report: { total: 1, counts: { passed: 0, failed: 0, error: 0 }, categories: {}, cases: [row] }, summary: {} })
const flush = async () => { for (let i=0;i<8;i++) await Promise.resolve(); await nextTick() }
function mount() { const app = renderer.createApp(PlanRunReport, { runId: 'run', projectId: 'project' }); app.provide(ssrContextKey, { modules: new Set() }); app.config.warnHandler = () => {}; const vm = app.mount({ children: [] }); return { state: (vm as any).$.setupState, stop: () => app.unmount() } }
beforeEach(() => {
  vi.clearAllMocks(); vi.stubGlobal('window', { addEventListener: vi.fn(), removeEventListener: vi.fn() })
  mocks.report.mockResolvedValue(report()); mocks.collaboration.mockResolvedValue({ comments: [], attachments: [] }); mocks.issues.mockResolvedValue([])
  mocks.comment.mockResolvedValue({}); mocks.result.mockResolvedValue({})
  mocks.confirm.mockImplementation(options => options.onCancel())
})
describe('冻结批次报告回填保护', () => {
  it('选择提及成员时拦住所有写入和切换',async()=>{const {state:s,stop}=mount();await flush();await s.openCase(row);s.comment='pending';s.defectTitle='pending defect';s.mentionBusy=true;await s.saveSummary();await s.saveResult();await s.upload({size:1} as File);await s.createDefect();await s.createShare();await s.revoke('share');await s.sendComment();await s.closeCase();for(const action of [mocks.summary,mocks.result,mocks.attachment,mocks.saveIssue,mocks.share,mocks.revoke,mocks.comment])expect(action).not.toHaveBeenCalled();expect(s.caseOpen).toBe(true);expect(s.comment).toBe('pending');stop()})
  it('发布评论成功后仍保护未保存步骤，取消关闭保留内容', async () => {
    const { state:s, stop } = mount(); await flush(); await s.openCase(row)
    s.stepRows[0].actual = 'unsaved'; s.comment = 'posted'; await s.sendComment()
    await s.closeCase(); expect(mocks.comment).toHaveBeenCalledWith('run','copy','posted')
    expect(mocks.confirm).toHaveBeenCalledTimes(1); expect(s.caseOpen).toBe(true); expect(s.stepRows[0].actual).toBe('unsaved'); stop()
  })
  it('保存结果在途阻止切换，成功后保留未发布评论', async () => {
    let finish!: () => void; mocks.result.mockReturnValue(new Promise<void>(resolve => { finish = resolve }))
    const { state:s, stop } = mount(); await flush(); await s.openCase(row); s.comment = 'keep me'
    const saving = s.saveResult(); await s.closeCase(); expect(s.caseOpen).toBe(true); expect(mocks.warning).toHaveBeenCalled()
    finish(); await saving; expect(s.caseOpen).toBe(true); expect(s.comment).toBe('keep me')
    expect(await s.beforeClose()).toBe(false); stop()
  })
  it('协作A迟到不能覆盖当前B附件', async () => {
    let finish!: (v:any) => void; mocks.collaboration.mockReturnValueOnce(new Promise(resolve => {finish=resolve})).mockResolvedValueOnce({ comments: [], attachments: [{id:'b',name:'B'}] })
    const { state:s, stop } = mount(); await flush(); const a=s.openCase(row); await flush()
    await s.openCase({...row,associationId:'second'}); finish({comments:[],attachments:[{id:'a',name:'A'}]}); await a
    expect(s.current.associationId).toBe('second'); expect(s.collab.attachments[0].id).toBe('b'); stop()
  })
  it('迟到的分享读取不能恢复已撤销条目', async () => {
    let finish!: (v:any) => void; mocks.shares.mockReturnValueOnce(new Promise(resolve => {finish=resolve})).mockResolvedValueOnce([{id:'share',revoked:true}])
    const {state:s,stop}=mount(); await flush(); const first=s.loadShares(); await s.loadShares(); finish([{id:'share',revoked:false}]); await first
    expect(s.shares[0].revoked).toBe(true); stop()
  })
  it('报告总结草稿阻止刷新读取和离开', async () => {
    const { state:s, stop } = mount(); await flush(); const calls=mocks.report.mock.calls.length
    s.summary.notes='unsaved'; await s.load(); expect(mocks.report).toHaveBeenCalledTimes(calls); expect(await s.beforeClose()).toBe(false); stop()
  })
})
