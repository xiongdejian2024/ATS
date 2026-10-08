import {describe,it,expect,vi,beforeEach} from 'vitest'
const mocks=vi.hoisted(()=>({folders:vi.fn(),files:vi.fn(),archive:vi.fn(),saveFolder:vi.fn(),upload:vi.fn(),warning:vi.fn(),error:vi.fn()}))
vi.mock('@/api/fileLibrary',()=>({fileLibraryApi:mocks}))
vi.mock('@/api/caseFeatures',()=>({saveCaseBlob:vi.fn()}))
vi.mock('ant-design-vue',()=>({message:{warning:mocks.warning,error:mocks.error}}))
vi.mock('@/stores/user',()=>({useUserStore:()=>({user:{id:'user'}})}))
import FileLibraryPicker from './FileLibraryPicker.vue'
import {componentHost,flushComponent as flush} from '@/test/componentHost'
const file=(id:string)=>({id,fileName:id,archived:false,published:true,fileSize:5})
beforeEach(()=>{vi.clearAllMocks();mocks.folders.mockResolvedValue([]);mocks.files.mockResolvedValue({items:[file('a')],total:1,canManage:true})})
describe('文件库选择与失败恢复',()=>{
 it('跨页保留文件并冻结返回副本',async()=>{const {state:s,stop}=componentHost(FileLibraryPicker,{projectId:'project'});const pending=s.pick();await flush();s.select(['a'],[file('a')]);mocks.files.mockResolvedValueOnce({items:[file('b')],total:21,canManage:true});s.paginate({current:2});await flush();s.select(['a','b'],[file('b')]);s.accept();expect((await pending).map((f:any)=>f.id)).toEqual(['a','b']);stop()})
 it('归档/目录保存失败保留选择和名称，可重试',async()=>{mocks.archive.mockRejectedValueOnce(new Error('synthetic'));mocks.saveFolder.mockRejectedValueOnce(new Error('synthetic'));const {state:s,stop}=componentHost(FileLibraryPicker,{projectId:'project'});const pending=s.pick();await flush();s.select(['a'],[file('a')]);await s.archive(file('a'));expect(s.selected).toEqual(['a']);s.newFolder();s.folderName='draft directory';await s.saveFolder();expect(s.folderOpen).toBe(true);expect(s.folderName).toBe('draft directory');s.cancel();expect(await pending).toEqual([]);stop()})
 it('切项目终止旧选择，旧读取不覆盖新的目录/文件',async()=>{let finish!:(v:any)=>void;mocks.files.mockReturnValueOnce(new Promise(r=>finish=r));const {state:s,props,stop}=componentHost(FileLibraryPicker,{projectId:'first'});const first=s.pick();props.projectId='second';await flush();expect(await first).toEqual([]);mocks.files.mockResolvedValueOnce({items:[file('new')],total:1,canManage:false});const second=s.pick();await flush();finish({items:[file('old')],total:1,canManage:true});await flush();expect(s.files[0].id).toBe('new');expect(s.canManage).toBe(false);s.cancel();await second;stop()})
})
