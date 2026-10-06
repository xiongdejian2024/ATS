/** 视图坐标不进入规划草稿；画布四周保留半屏空间，边缘节点也可居中。 */
export type MinderMode = "right" | "default" | "filetree";
export interface MinderBox {
  x: number;
  y: number;
  width: number;
  height: number;
}
export interface MinderGeometry {
  width: number;
  height: number;
  nodes: Record<string, MinderBox>;
  paths: string[];
  offset: { x: number; y: number };
}
export const minderModes: { value: MinderMode; label: string }[] = [
  { value: "right", label: "右向布局" },
  { value: "default", label: "左右分支布局" },
  { value: "filetree", label: "目录树布局" },
];
export function isMinderMode(value: unknown): value is MinderMode {
  return minderModes.some((mode) => mode.value === value);
}
export function zoomScroll(scroll: number, before: number, after: number) {
  return (scroll / before) * after;
}
export function cameraScroll(center: number, zoom: number) {
  return center * zoom;
}
export function visibleMinderBox(
  left: number,
  top: number,
  width: number,
  height: number,
  zoom: number,
): MinderBox {
  return {
    x: (left - width / 2) / zoom,
    y: (top - height / 2) / zoom,
    width: width / zoom,
    height: height / zoom,
  };
}
