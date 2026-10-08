import { describe, expect, it, vi } from 'vitest'
const client = vi.hoisted(() => ({ get: vi.fn(), post: vi.fn(), put: vi.fn() }))
vi.mock('@/utils/api', () => ({ apiClient: client }))
import { scriptJobsApi, scriptRunPath } from './scriptJobs'
describe('independent script job API contract', () => {
  it('uses project scope and pagination for jobs and node eligibility', async () => {
    await scriptJobsApi.list('project', 2); await scriptJobsApi.nodes('project')
    expect(client.get).toHaveBeenCalledWith('/script-jobs', { params: { projectId: 'project', page: 2, size: 20 }, signal: undefined })
    expect(client.get).toHaveBeenCalledWith('/script-jobs/nodes', { params: { projectId: 'project' }, signal: undefined })
  })
  it('uses requestId and exact immutable run endpoints without a testcase or current node', async () => {
    await scriptJobsApi.run('job', 'stable-request')
    await scriptJobsApi.cancel('job', 'frozen-run')
    await scriptJobsApi.resolve('job', 'frozen-run', 'checked')
    expect(client.post).toHaveBeenCalledWith('/script-jobs/job/runs', { requestId: 'stable-request' })
    expect(client.post).toHaveBeenCalledWith('/script-jobs/job/runs/frozen-run/cancel', {})
    expect(client.post).toHaveBeenCalledWith('/script-jobs/job/runs/frozen-run/resolve', { confirmedStopped: true, reason: 'checked' })
  })
  it('bounds log reads and encodes run identities', async () => {
    const signal = new AbortController().signal
    await scriptJobsApi.logs('job/a', 'run/a', signal)
    expect(scriptRunPath('job/a', 'run/a')).toBe('/script-jobs/job%2Fa/runs/run%2Fa')
    expect(client.get).toHaveBeenCalledWith('/script-jobs/job%2Fa/runs/run%2Fa/logs', { params: { skip: 0, limit: 20 }, signal })
  })
})
