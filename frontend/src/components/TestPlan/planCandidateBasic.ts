import { bluePalette } from "@/styles/theme";
import type { CandidateCondition } from "@/api/planCaseWorkspace";

/** 官方请求方式顺序；未认识的插件方式仍按真实文本显示。 */
export const requestMethods = [
  "GET",
  "POST",
  "PUT",
  "DELETE",
  "PATCH",
  "OPTIONS",
  "HEAD",
  "CONNECT",
];
export function methodColor(method?: string | null) {
  if (["GET", "HEAD", "HTTP"].includes(method || "")) return "#00a870";
  if (method === "POST") return "#d88100";
  if (method === "DELETE") return "#f53f3f";
  if (method === "PATCH") return bluePalette.primary;
  if (method === "CONNECT") return "#bb81ce";
  return "#165dff";
}
export function basicCondition(
  query: CandidateCondition,
): Partial<CandidateCondition> {
  return {
    ...(query.protocols === undefined
      ? {}
      : { protocols: [...query.protocols] }),
    ...(query.methods?.length ? { methods: [...query.methods] } : {}),
    ...(query.createdBy?.length ? { createdBy: [...query.createdBy] } : {}),
  };
}
export function protocolStorageKey(userId: string) {
  return `ats:associate-protocols:${encodeURIComponent(userId)}`;
}
/** 保存排除的协议，新出现的真实协议默认可见；不记录令牌或实体内容。 */
export function readProtocols(
  storage: Pick<Storage, "getItem">,
  key: string,
  options: string[],
): string[] | undefined {
  try {
    const raw = storage.getItem(key);
    const excluded = raw ? JSON.parse(raw) : [];
    if (!Array.isArray(excluded) || excluded.some((v) => typeof v !== "string"))
      throw new Error("协议偏好格式无效");
    const selected = options.filter((p) => !excluded.includes(p));
    return selected.length === options.length ? undefined : selected;
  } catch (exception) {
    console.error("读取关联协议偏好失败，使用全部协议", exception);
    return undefined;
  }
}
export function writeProtocols(
  storage: Pick<Storage, "setItem">,
  key: string,
  options: string[],
  selected?: string[],
) {
  try {
    storage.setItem(
      key,
      JSON.stringify(
        selected === undefined
          ? []
          : options.filter((p) => !selected.includes(p)),
      ),
    );
    console.info("关联协议筛选已保存", {
      选择协议: selected === undefined ? "全部" : selected,
    });
  } catch (exception) {
    console.error("保存关联协议偏好失败，当前选择继续有效", exception);
  }
}
