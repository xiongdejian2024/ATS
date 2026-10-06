import { ref, computed, type Ref } from "vue";
import { useEventListener } from "@vueuse/core";
import { intersects } from "./planMinderSelection";

/** 在已有DOM脑图上做框选；坐标沿画布滚动内容，节点盒使用实际缩放后的尺寸。 */
export function useMinderMarquee(
  viewport: Ref<HTMLElement | undefined>,
  canSelect: () => boolean,
  select: (ids: string[]) => void,
) {
  const rectangle = ref<{
    left: number;
    top: number;
    width: number;
    height: number;
  }>();
  let gesture: { pointerId: number; x: number; y: number } | undefined;
  const style = computed(
    () =>
      rectangle.value &&
      Object.fromEntries(
        Object.entries(rectangle.value).map(([key, value]) => [
          key,
          `${value}px`,
        ]),
      ),
  );
  function cancel() {
    const element = viewport.value;
    if (gesture && element?.hasPointerCapture(gesture.pointerId))
      element.releasePointerCapture(gesture.pointerId);
    gesture = undefined;
    rectangle.value = undefined;
  }
  function start(event: PointerEvent) {
    if (
      event.pointerType !== "mouse" ||
      event.button !== 0 ||
      event.altKey ||
      (event.target as HTMLElement)?.closest(
        "button, input, select, textarea, [role=toolbar], [role=listbox], [contenteditable=true]",
      ) ||
      !viewport.value ||
      !canSelect()
    )
      return;
    const element = viewport.value,
      bounds = element.getBoundingClientRect();
    cancel();
    gesture = {
      pointerId: event.pointerId,
      x: event.clientX - bounds.left + element.scrollLeft,
      y: event.clientY - bounds.top + element.scrollTop,
    };
    select([]);
    element.focus({ preventScroll: true });
    element.setPointerCapture(event.pointerId);
    event.preventDefault();
  }
  function move(event: PointerEvent) {
    if (!gesture || event.pointerId !== gesture.pointerId || !viewport.value)
      return;
    if (!canSelect()) {
      cancel();
      return;
    }
    const element = viewport.value,
      bounds = element.getBoundingClientRect();
    const x =
      Math.min(bounds.right, Math.max(bounds.left, event.clientX)) -
      bounds.left +
      element.scrollLeft;
    const y =
      Math.min(bounds.bottom, Math.max(bounds.top, event.clientY)) -
      bounds.top +
      element.scrollTop;
    if (!rectangle.value && Math.hypot(x - gesture.x, y - gesture.y) < 10)
      return;
    rectangle.value = {
      left: Math.min(x, gesture.x),
      top: Math.min(y, gesture.y),
      width: Math.abs(x - gesture.x),
      height: Math.abs(y - gesture.y),
    };
    const region = {
      left: rectangle.value.left + bounds.left - element.scrollLeft,
      top: rectangle.value.top + bounds.top - element.scrollTop,
      right:
        rectangle.value.left +
        rectangle.value.width +
        bounds.left -
        element.scrollLeft,
      bottom:
        rectangle.value.top +
        rectangle.value.height +
        bounds.top -
        element.scrollTop,
    };
    const ids = [
      ...element.querySelectorAll<HTMLElement>(".branch-label > .minder-node"),
    ]
      .filter(
        (node) =>
          intersects(node.getBoundingClientRect(), bounds) &&
          intersects(node.getBoundingClientRect(), region),
      )
      .map(
        (node) =>
          node.closest<HTMLElement>(".minder-branch[data-node-id]")!.dataset
            .nodeId!,
      );
    select(ids);
    window.getSelection()?.removeAllRanges();
  }
  useEventListener(viewport, "pointermove", move);
  useEventListener(
    viewport,
    ["pointerup", "pointercancel", "lostpointercapture"],
    cancel,
  );
  return { start, cancel, style, active: computed(() => !!rectangle.value) };
}
