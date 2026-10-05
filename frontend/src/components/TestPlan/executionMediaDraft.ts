import type { MediaCleanup } from "@/api/planCaseMedia";

/** 跟踪本次编辑上传的图片；跨页签保存，按原计划收尾，不触碰历史文件。 */
export class ExecutionMediaDraft {
  private files = new Map<string, { planId: string; id: string }>();
  private pending: Promise<void> = Promise.resolve();
  constructor(
    private remove: (planId: string, ids: string[]) => Promise<MediaCleanup>,
  ) {}
  track(planId: string, id: string) {
    this.files.set(`${planId}:${id}`, { planId, id });
  }
  get size() {
    return this.files.size;
  }
  cleanup(): Promise<void> {
    const snapshot = [...this.files.entries()];
    this.pending = this.pending.then(async () => {
      const groups = new Map<string, typeof snapshot>();
      for (const entry of snapshot) {
        const planId = entry[1].planId;
        groups.set(planId, [...(groups.get(planId) || []), entry]);
      }
      for (const [planId, entries] of groups) {
        for (let start = 0; start < entries.length; start += 500) {
          const batch = entries.slice(start, start + 500);
          try {
            const outcome = await this.remove(
              planId,
              batch.map(([, item]) => item.id),
            );
            const settled = new Set([
              ...outcome.removed,
              ...outcome.retained,
              ...outcome.missing,
            ]);
            for (const [key, item] of batch)
              if (settled.has(item.id) && this.files.get(key) === item)
                this.files.delete(key);
          } catch (error) {
            console.error("清理未提交执行图片失败，保留待重试编号", error);
          }
        }
      }
    });
    return this.pending;
  }
}
