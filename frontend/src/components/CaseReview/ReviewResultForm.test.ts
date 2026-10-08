import {describe,it,expect,vi,beforeEach} from 'vitest'
const mocks=vi.hoisted(()=>({confirm:vi.fn(),warning:vi.fn()}))
vi.mock('ant-design-vue',()=>({Modal:{confirm:mocks.confirm},message:{warning:mocks.warning}}))
vi.mock('@/components/TestCase/CaseRichText.vue',()=>({default:{render:()=>null}}))
vi.mock('@/components/TestCase/FileLibraryPicker.vue',()=>({default:{render:()=>null}}))
vi.mock('@/api/fileLibrary',()=>({fileLibraryApi:{}}))
import ReviewResultForm from './ReviewResultForm.vue'
import {componentHost,flushComponent as flush} from '@/test/componentHost'
beforeEach(()=>{vi.clearAllMocks();vi.stubGlobal('window',{addEventListener:vi.fn(),removeEventListener:vi.fn()});mocks.confirm.mockImplementation(options=>options.onCancel())})
describe('评审素材和理由事务',()=>{
 it('上传中拒绝离开，上传结束恢复；附件随准确结论提交',async()=>{const submit=vi.fn().mockResolvedValue(undefined);const {state:s,stop}=componentHost(ReviewResultForm,{projectId:'project',submitResult:submit});s.setUploading(true);expect(await s.beforeClose()).toBe(false);s.setUploading(false);s.reason='proof';s.files=[{id:'file',fileName:'evidence'}];await s.submit();expect(submit).toHaveBeenCalledWith('approved','proof',['file']);expect(s.reason).toBe('');expect(s.files).toEqual([]);expect(await s.beforeClose()).toBe(true);stop()})
 it('提交失败保留理由及文件，取消离开继续编辑',async()=>{const submit=vi.fn().mockRejectedValue(new Error('synthetic'));const {state:s,stop}=componentHost(ReviewResultForm,{projectId:'project',submitResult:submit});s.reason='keep';s.files=[{id:'file',fileName:'proof'}];await s.submit();await flush();expect(s.reason).toBe('keep');expect(s.files[0].id).toBe('file');expect(await s.beforeClose()).toBe(false);expect(s.saving).toBe(false);stop()})
})
