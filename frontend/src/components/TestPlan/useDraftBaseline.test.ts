import { reactive } from 'vue'
import { describe, expect, it } from 'vitest'
import { useDraftBaseline } from './useDraftBaseline'
describe('报告分别确认已持久字段', () => {
  it('评论成功不能解除未保存步骤的离开保护', () => {
    const form = reactive({ steps: [{ actual: '' }], notes: '', comment: '', defectTitle: '' })
    const draft = useDraftBaseline(() => form); draft.acknowledge()
    form.steps[0].actual = 'unsaved evidence'; form.comment = 'posted'
    form.comment = ''; draft.acknowledge(['comment'])
    expect(draft.dirty.value).toBe(true); expect(form.steps[0].actual).toBe('unsaved evidence')
  })
  it('结果保存保留未发布评论和缺陷标题保护', () => {
    const form = reactive({ steps: ['pending'], notes: '', comment: '', defectTitle: '' })
    const draft = useDraftBaseline(() => form); draft.acknowledge()
    form.steps = ['passed']; form.notes = 'persisted'; form.comment = 'draft'; form.defectTitle = 'issue'
    draft.acknowledge(['steps','notes']); expect(draft.dirty.value).toBe(true)
    form.comment = ''; draft.acknowledge(['comment']); expect(draft.dirty.value).toBe(true)
    form.defectTitle = ''; draft.acknowledge(['defectTitle']); expect(draft.dirty.value).toBe(false)
  })
})
