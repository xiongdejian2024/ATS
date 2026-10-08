import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { bluePalette, atsBlueTheme } from "./theme";
const css = readFileSync(new URL("./index.css", import.meta.url), "utf8");
function luminance(hex: string) {
  const channels = hex
    .replace("#", "")
    .match(/../g)!
    .map((x) => parseInt(x, 16) / 255)
    .map((x) => (x <= 0.04045 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4));
  return channels[0] * 0.2126 + channels[1] * 0.7152 + channels[2] * 0.0722;
}
function contrast(a: string, b: string) {
  const x = luminance(a),
    y = luminance(b);
  return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
}
describe("ATS蓝色主色与可读性", () => {
  it("主色、链接、交互态使用同一蓝色令牌", () => {
    expect(atsBlueTheme.token.colorPrimary).toBe(bluePalette.primary);
    expect(atsBlueTheme.token.colorLink).toBe(bluePalette.primary);
    expect(atsBlueTheme.token.colorLinkHover).toBe(bluePalette.hover);
    expect(atsBlueTheme.token.colorPrimaryActive).toBe(bluePalette.active);
    for (const color of Object.values(bluePalette))
      expect(css.toLowerCase()).toContain(color);
  });
  it("白色按钮文本在默认、悬浮和激活蓝色上均达到4.5:1", () => {
    for (const background of [
      bluePalette.primary,
      bluePalette.hover,
      bluePalette.active,
    ])
      expect(
        contrast(bluePalette.onPrimary, background),
      ).toBeGreaterThanOrEqual(4.5);
  });
  it("蓝色链接在白色、页面底色和浅蓝选中态上均达到4.5:1", () => {
    for (const background of [
      "#ffffff",
      "#f2f3f5",
      bluePalette.soft,
      bluePalette.selected,
    ])
      expect(contrast(bluePalette.primary, background)).toBeGreaterThanOrEqual(
        4.5,
      );
    expect(contrast(bluePalette.focus, "#ffffff")).toBeGreaterThanOrEqual(3);
  });
  it("不覆盖红色危险按钮或成功/警告语义，系统偏好不会启用不完整暗色", () => {
    expect(css).toContain(
      ".ant-btn-primary:not(:disabled):not(.ant-btn-dangerous)",
    );
    expect(css).toContain("--success-gradient:#00b42a");
    expect(css).toContain("--warning-gradient:#ff7d00");
    expect(css).toContain("--error-gradient:#f53f3f");
    expect(css).toContain("color-scheme:light");
    expect(css).not.toContain("#811fa3");
  });
});
