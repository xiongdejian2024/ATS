import { describe, it, expect } from "vitest";
import { caseFolderTree } from "../planCaseFolders";
describe("功能用例目录", () => {
  it("搜索子模块保留祖先与真实数量，排除其他分支", () => {
    const rows = [
      { id: "root", name: "发布", count: 3 },
      { id: "child", parentId: "root", name: "接口", count: 2 },
      { id: "other", name: "界面", count: 1 },
    ];
    const tree = caseFolderTree(rows, "接口");
    expect(tree.length).toBe(1);
    expect(tree[0].count).toBe(3);
    expect(tree[0].children?.[0].id).toBe("child");
  });
  it("损坏父链无无限递归，孤立目录可访问", () => {
    const rows = [
      { id: "a", parentId: "b", name: "甲", count: 0 },
      { id: "b", parentId: "a", name: "乙", count: 0 },
      { id: "c", parentId: "missing", name: "丙", count: 1 },
    ];
    const tree = caseFolderTree(rows);
    expect(tree.length).toBe(2);
    expect(JSON.stringify(tree)).toContain("丙");
    expect(caseFolderTree(rows, "甲")[0].children?.length).toBe(1);
  });
});
