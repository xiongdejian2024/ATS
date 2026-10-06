/** 关联接口与接口用例使用官方默认列；扩展字段在表格设置中单独开启。 */
export function planCandidateColumns(resourceType: "API" | "CASE") {
  const column = (
    key: string,
    title: string,
    width: number,
    visible = true,
    sorter = false,
  ) => ({
    key,
    dataIndex: key,
    title,
    width,
    defaultVisible: visible,
    sorter,
    required: ["id", "caseCode", "name"].includes(key),
  });
  return resourceType === "API"
    ? [
        column("id", "ID", 100, true, true),
        column("name", "接口名称", 200, true, true),
        column("method", "请求方式", 140),
        column("path", "路径", 200),
        column("tags", "标签", 216),
        column("caseTotal", "用例数", 100),
        column("createdByName", "创建人", 200),
        column("createdAt", "创建时间", 200, false, true),
        column("nativeState", "状态", 150, false),
      ]
    : [
        column("caseCode", "ID", 100, true, true),
        column("name", "用例名称", 180, true, true),
        column("priority", "用例等级", 150),
        column("lastReportStatus", "最近执行结果", 150, false),
        column("path", "路径", 200),
        column("tags", "标签", 300),
        column("createdByName", "创建人", 200),
        column("createdAt", "创建时间", 200, true, true),
        column("nativeState", "状态", 150, false),
        column("protocol", "协议", 150, false),
        column("moduleName", "所属模块", 200, false),
        column("environmentLabel", "用例环境", 200, false),
      ];
}
