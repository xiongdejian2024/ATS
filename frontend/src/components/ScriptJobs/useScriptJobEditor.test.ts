import { describe, expect, it, vi } from 'vitest'
import { effectScope, reactive } from 'vue'
vi.mock('@/utils/api', () => ({ apiClient: {} }))
import { useScriptJobEditor, type ScriptEditorSource } from './useScriptJobEditor'
import { fixtureJob as job, fixtureNode as node, deferred } from './scriptJobFixtures'
import { nodeBlock, validateScriptJob } from './scriptJobState'
import type { ScriptJob, ScriptJobConfig, ScriptMode } from '@/api/scriptJobs'

describe('脚本配置与编辑生命周期', () => {
  it('accepts offline queues and distinguishes online incompatible agents', () => {
    expect(nodeBlock(node({ isOnline: false, supportsScriptJobs: false }))).toBe('')
    expect(nodeBlock(node({ supportsScriptJobs: false }))).toContain('升级')
    expect(nodeBlock(undefined)).toContain('权限')
  })
  it.each(['../outside', '/absolute', 'C:\\windows', 'build/../../outside', '\\\\server\\share'])('rejects workspace escapes: %s', workDir => {
    expect(validateScriptJob({ ...job(), workDir })).toContain('工作目录')
  })
  it('enforces finite timeout and UTF-8 script limits before sending', () => {
    expect(validateScriptJob({ ...job(), timeoutSeconds: Infinity })).toContain('超时')
    expect(validateScriptJob({ ...job(), timeoutSeconds: 0 })).toContain('超时')
    expect(validateScriptJob({ ...job(), script: '中'.repeat(22000) })).toContain('64 KiB')
    expect(validateScriptJob({ ...job(), workDir: 'build/output', timeoutSeconds: 86400 })).toBe('')
  })
  it('creates exact argv including whitespace and empty arguments, suppresses duplicate saves', async () => {
    const source = reactive<ScriptEditorSource>({ open: true, projectId: 'project-a', job: null, nodes: [node({ isOnline: false })] })
    const pending = deferred<ScriptJob>(), api = { create: vi.fn((_config: ScriptJobConfig) => pending.promise) }, events = { close: vi.fn(), saved: vi.fn() }
    const scope = effectScope(), editor = scope.run(() => useScriptJobEditor(source, events, api as any))!
    editor.form.value = { ...job(), mode: 'command', command: 'python3', args: ['file with spaces.py', '', '  retained  '] }
    const saving = editor.save(); await editor.save()
    expect(api.create).toHaveBeenCalledOnce()
    expect(api.create.mock.calls[0][0]).toMatchObject({ args: ['file with spaces.py', '', '  retained  '], script: '', command: 'python3' })
    pending.resolve(job()); await saving
    expect(events.saved).toHaveBeenCalledOnce()
    scope.stop()
  })
  it('close/reopen isolates old save completion from a new draft', async () => {
    const source = reactive<ScriptEditorSource>({ open: true, projectId: 'project-a', job: job(), nodes: [node()] })
    const pending = deferred<ScriptJob>(), api = { update: vi.fn(() => pending.promise) }, events = { close: vi.fn(), saved: vi.fn() }
    const scope = effectScope(), editor = scope.run(() => useScriptJobEditor(source, events, api as any))!
    const saving = editor.save()
    source.open = false; source.job = job('job-b'); source.open = true
    pending.resolve(job()); await saving
    expect(events.saved).not.toHaveBeenCalled()
    expect(editor.form.value.name).toBe('job-b')
    expect(editor.saving.value).toBe(false)
    scope.stop()
  })
  it.each<ScriptMode>(['shell', 'python', 'command'])('renaming a %s job preserves existing exact arguments on save/reopen', async mode => {
    const original = { ...job(), mode, script: mode === 'command' ? '' : 'print("script")', command: mode === 'command' ? 'python3' : '', args: ['--name', 'hello world', '', '  retained  '] }
    const source = reactive<ScriptEditorSource>({ open: true, projectId: 'project-a', job: original, nodes: [node()] })
    const api = { update: vi.fn(async (_id: string, config: Omit<ScriptJobConfig, 'projectId'>) => ({ ...original, ...config })) }
    const scope = effectScope(), editor = scope.run(() => useScriptJobEditor(source, { close: vi.fn(), saved: saved => { source.job = saved; source.open = false } }, api as any))!
    editor.form.value.name = 'renamed'
    await editor.save()
    expect(api.update.mock.calls[0][1].args).toEqual(original.args)
    expect(api.update.mock.calls[0][1].name).toBe('renamed')
    source.open = true
    expect(editor.form.value.args).toEqual(original.args)
    editor.form.value.args[1] = 'new argument with spaces'; editor.form.value.args.push('last')
    await editor.save()
    expect(api.update.mock.calls[1][1].args).toEqual(['--name', 'new argument with spaces', '', '  retained  ', 'last'])
    expect(original.args).toEqual(['--name', 'hello world', '', '  retained  '])
    scope.stop()
  })
})
