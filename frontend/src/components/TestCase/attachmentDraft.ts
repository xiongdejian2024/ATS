/** 分项确认附件写入；失败时保留未完成操作，重试不会重传已确认的文件。 */
export async function flushAttachmentDraft<T extends { id: string }>(
  pending: T[],
  removed: string[],
  upload: (item: T) => Promise<void>,
  remove: (id: string) => Promise<void>,
): Promise<void> {
  for (const item of [...pending]) {
    await upload(item);
    const index = pending.findIndex((entry) => entry.id === item.id);
    if (index >= 0) pending.splice(index, 1);
  }
  for (const id of [...removed]) {
    await remove(id);
    const index = removed.indexOf(id);
    if (index >= 0) removed.splice(index, 1);
  }
}
