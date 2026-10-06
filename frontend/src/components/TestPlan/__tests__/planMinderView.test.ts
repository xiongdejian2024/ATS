import { describe, expect, it } from "vitest";
import {
  cameraScroll,
  isMinderMode,
  minderModes,
  visibleMinderBox,
  zoomScroll,
} from "../planMinderView";

describe("脑图视图坐标", () => {
  it("仅提供MS规划实际开放的三种布局", () => {
    expect(minderModes.map((mode) => mode.value)).toEqual([
      "right",
      "default",
      "filetree",
    ]);
    expect(isMinderMode("fishbone")).toBe(false);
    expect(isMinderMode(null)).toBe(false);
    expect(isMinderMode("filetree")).toBe(true);
  });
  it.each([0.25, 0.5, 1, 2])(
    "在缩放%s下根节点居中与缩略图定位使用相同坐标",
    (zoom) => {
      const center = { x: 340, y: 610 };
      const box = visibleMinderBox(
        cameraScroll(center.x, zoom),
        cameraScroll(center.y, zoom),
        1100,
        660,
        zoom,
      );
      expect(box.x + box.width / 2).toBeCloseTo(center.x);
      expect(box.y + box.height / 2).toBeCloseTo(center.y);
    },
  );
  it.each([
    [0.25, 2],
    [2, 0.5],
    [0.5, 1],
  ])("从%s缩放到%s时保留当前视图中心", (before, after) => {
    const oldBox = visibleMinderBox(680, 930, 1100, 660, before);
    const box = visibleMinderBox(
      zoomScroll(680, before, after),
      zoomScroll(930, before, after),
      1100,
      660,
      after,
    );
    expect(box.x + box.width / 2).toBeCloseTo(oldBox.x + oldBox.width / 2);
    expect(box.y + box.height / 2).toBeCloseTo(oldBox.y + oldBox.height / 2);
  });
});
