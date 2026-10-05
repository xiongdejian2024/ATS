/** 独立审阅的可持久化列表范围和提交后选中位置。 */
export const reviewStates = [
  { value: "approved", label: "通过" },
  { value: "rejected", label: "不通过" },
  { value: "under_review", label: "评审中" },
  { value: "un_review", label: "未评审" },
  { value: "re_review", label: "重新提审" },
];
export const reviewStateName = (state: string) =>
  reviewStates.find((s) => s.value === state)?.label || state;
export const reviewStateColor = (state: string) =>
  ({
    approved: "green",
    rejected: "red",
    under_review: "orange",
    re_review: "orange",
    un_review: "blue",
  })[state] || "default";
/** 多结果优先；兼容旧单结果地址，显式清空多结果时不恢复旧值。 */
export function selectedReviewStates(scope: Record<string, any>): string[] {
  const values = Array.isArray(scope.states)
    ? scope.states
    : scope.state
      ? [scope.state]
      : [];
  return [
    ...new Set<string>(
      values.filter((state: unknown) =>
        reviewStates.some((option) => option.value === state),
      ),
    ),
  ];
}
export function readingScope(value: unknown): Record<string, any> {
  let data: Record<string, any> = {};
  try {
    data = typeof value === "string" ? JSON.parse(value) : value || {};
  } catch (error) {
    console.error("审阅列表范围解析失败，使用默认范围", error);
  }
  const result: Record<string, any> = {
    page: 1,
    size: 10,
    sort: "createdAt",
    order: "desc",
    folder: "all",
    view: "list",
  };
  if (!data || typeof data !== "object" || Array.isArray(data)) return result;
  for (const field of ["page", "size"]) {
    const number = Number(data[field]);
    if (
      Number.isInteger(number) &&
      number >= 1 &&
      (field !== "size" || number <= 100)
    )
      result[field] = number;
  }
  for (const field of [
    "search",
    "folder",
    "priority",
    "reviewerId",
    "creatorId",
    "state",
  ]) {
    if (typeof data[field] === "string" && data[field].length <= 255)
      result[field] = data[field];
  }
  if (["createdAt", "caseCode", "name"].includes(data.sort))
    result.sort = data.sort;
  if (["asc", "desc"].includes(data.order)) result.order = data.order;
  for (const field of ["includeDescendants", "onlyMine"])
    if (typeof data[field] === "boolean") result[field] = data[field];
  if (Array.isArray(data.states))
    result.states = data.states.filter((state: unknown) =>
      reviewStates.some((option) => option.value === state),
    );
  return result;
}
export function afterReviewTarget(
  previous: string[],
  active: string,
  current: string[],
  autoNext: boolean,
) {
  if (!autoNext) return current.length ? active : undefined;
  const oldIndex = previous.indexOf(active),
    index = current.indexOf(active);
  // 当前条目被结果筛选移除时，新列表同一位置就是后一条。
  return index < 0
    ? current[oldIndex] || current[0]
    : current[index + 1] || active;
}
