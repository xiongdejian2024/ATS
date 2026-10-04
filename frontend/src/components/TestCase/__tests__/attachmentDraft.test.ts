import { describe, expect, it, vi } from 'vitest';
import { flushAttachmentDraft } from '../attachmentDraft';

describe('附件保存失败后的分项重试', () => {
  it('第二个上传失败后保留剩余附件，重试跳过第一个已保存文件', async () => {
    const pending = [{ id: 'a' }, { id: 'b' }], removed = ['old'];
    const upload = vi.fn().mockResolvedValueOnce(undefined).mockRejectedValueOnce(new Error('网络失败')).mockResolvedValue(undefined);
    const remove = vi.fn().mockResolvedValue(undefined);
    await expect(flushAttachmentDraft(pending, removed, upload, remove)).rejects.toThrow('网络失败');
    expect(pending.map(x => x.id)).toEqual(['b']);
    expect(remove).not.toHaveBeenCalled();
    await flushAttachmentDraft(pending, removed, upload, remove);
    expect(upload.mock.calls.map(([x]) => x.id)).toEqual(['a', 'b', 'b']);
    expect(pending).toEqual([]);
    expect(removed).toEqual([]);
  });
  it('删除失败不会重传文件或重复删除已确认附件', async () => {
    const pending = [{ id: 'a' }], removed = ['x', 'y'];
    const upload = vi.fn().mockResolvedValue(undefined);
    const remove = vi.fn().mockResolvedValueOnce(undefined).mockRejectedValueOnce(new Error('删除失败')).mockResolvedValue(undefined);
    await expect(flushAttachmentDraft(pending, removed, upload, remove)).rejects.toThrow('删除失败');
    expect(removed).toEqual(['y']);
    await flushAttachmentDraft(pending, removed, upload, remove);
    expect(upload).toHaveBeenCalledTimes(1);
    expect(remove.mock.calls.map(([id]) => id)).toEqual(['x', 'y', 'y']);
  });
});
