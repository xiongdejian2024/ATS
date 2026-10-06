import { ref, watch, type Ref } from "vue";
import { useEventListener } from "@vueuse/core";
/** 手形模式与框选互斥，通过原生指针捕获支持鼠标和触控画布移动。 */
export function useMinderPan(
  viewport: Ref<HTMLElement | undefined>,
  enabled: Ref<boolean>,
) {
  const moved = ref(false);
  let gesture:
    | { pointerId: number; x: number; y: number; left: number; top: number }
    | undefined;
  function cancel() {
    if (gesture && viewport.value?.hasPointerCapture(gesture.pointerId))
      viewport.value.releasePointerCapture(gesture.pointerId);
    gesture = undefined;
  }
  function start(event: PointerEvent) {
    if (
      !enabled.value ||
      event.button !== 0 ||
      !viewport.value ||
      (event.target as HTMLElement)?.closest("input, textarea, [role=toolbar]")
    )
      return;
    const element = viewport.value;
    moved.value = false;
    gesture = {
      pointerId: event.pointerId,
      x: event.clientX,
      y: event.clientY,
      left: element.scrollLeft,
      top: element.scrollTop,
    };
    element.setPointerCapture(event.pointerId);
    event.preventDefault();
    event.stopPropagation();
  }
  useEventListener(viewport, "pointerdown", start, { capture: true });
  useEventListener(viewport, "pointermove", (event) => {
    if (!gesture || event.pointerId !== gesture.pointerId || !viewport.value)
      return;
    const dx = event.clientX - gesture.x,
      dy = event.clientY - gesture.y;
    if (Math.hypot(dx, dy) > 5) moved.value = true;
    viewport.value.scrollLeft = gesture.left - dx;
    viewport.value.scrollTop = gesture.top - dy;
  });
  useEventListener(
    viewport,
    "click",
    (event) => {
      if (enabled.value && moved.value) {
        event.preventDefault();
        event.stopPropagation();
      }
    },
    { capture: true },
  );
  useEventListener(
    viewport,
    ["pointerup", "pointercancel", "lostpointercapture"],
    cancel,
  );
  watch(enabled, cancel);
  return { cancel };
}
