import { onScopeDispose, watch, type Ref } from "vue";
import { throttle } from "lodash-es";
import type { TableDisplay } from "./tableDisplay";
import { columnMinWidth } from "./tableDisplay";

/** 复用表格原生拖动；合并最新显示设置，切换项目时取消旧上下文的延迟保存。 */
export function useTableColumnResize(
  display: Ref<TableDisplay>,
  storageKey: Ref<string>,
  persist: (next: TableDisplay) => boolean,
) {
  const pending = new Map<string, number>();
  const save = throttle(() => {
    const widths = Object.fromEntries(pending);
    const next = {
      ...display.value,
      columns: display.value.columns.map((column) =>
        pending.has(column.key)
          ? { ...column, width: pending.get(column.key) }
          : column,
      ),
    };
    pending.clear();
    if (persist(next))
      console.info("表格列宽已保存", { 表格: storageKey.value, 列宽: widths });
  }, 200);
  watch(
    storageKey,
    () => {
      save.cancel();
      pending.clear();
    },
    { flush: "sync" },
  );
  onScopeDispose(() => {
    save.flush();
    save.cancel();
  });
  return (width: number, column: { key?: string | number }) => {
    const key = String(column.key ?? "");
    if (
      !Number.isFinite(width) ||
      width <= 0 ||
      !display.value.columns.some((item) => item.key === key)
    )
      return;
    pending.set(key, Math.max(columnMinWidth(key), width));
    save();
  };
}
