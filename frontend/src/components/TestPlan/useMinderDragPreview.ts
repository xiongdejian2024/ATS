import { onScopeDispose } from "vue";
import { useEventListener } from "@vueuse/core";
export interface MinderDragEvent {
  item: HTMLElement;
  originalEvent?: MouseEvent | TouchEvent;
}
/** Sortable负责排序；这里只把body拖拽预览转换为真实屏幕坐标，避免SVG布局缩放使预览漂移。 */
export function useMinderDragPreview() {
  let gesture:
    | {
        rect: DOMRect;
        x: number;
        y: number;
        width: number;
        height: number;
        scale: number;
        id?: string;
      }
    | undefined;
  let pointer: { x: number; y: number } | undefined, frame: number | undefined;
  function position(event: MouseEvent | TouchEvent) {
    const point = "touches" in event ? event.touches[0] : event;
    return point ? { x: point.clientX, y: point.clientY } : undefined;
  }
  function choose(event: MinderDragEvent) {
    if (!event.originalEvent) return;
    const point = position(event.originalEvent);
    if (!point) return;
    const rect = event.item.getBoundingClientRect(),
      width = event.item.offsetWidth;
    gesture = {
      rect,
      ...point,
      width,
      height: event.item.offsetHeight,
      scale: width ? rect.width / width : 1,
      id: event.item.dataset.nodeId,
    };
    pointer = point;
  }
  function draw() {
    frame = undefined;
    if (!gesture || !pointer) return;
    const ghost = document.querySelector<HTMLElement>(".sortable-fallback");
    if (!ghost || ghost.dataset.nodeId !== gesture.id) return;
    Object.assign(ghost.style, {
      left: `${gesture.rect.x + pointer.x - gesture.x}px`,
      top: `${gesture.rect.y + pointer.y - gesture.y}px`,
      width: `${gesture.width}px`,
      height: `${gesture.height}px`,
      transform: `scale(${gesture.scale})`,
      transformOrigin: "0 0",
    });
  }
  function start() {
    frame = requestAnimationFrame(draw);
  }
  function move(event: MouseEvent | TouchEvent) {
    if (!gesture) return;
    pointer = position(event);
    if (frame === undefined) frame = requestAnimationFrame(draw);
  }
  function end() {
    if (frame !== undefined) cancelAnimationFrame(frame);
    frame = undefined;
    gesture = undefined;
    pointer = undefined;
  }
  useEventListener(document, ["pointermove", "mousemove", "touchmove"], move, {
    passive: true,
  });
  onScopeDispose(end);
  return { choose, start, end };
}
