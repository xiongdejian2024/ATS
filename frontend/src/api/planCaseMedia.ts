import { apiClient } from "@/utils/api";
export interface PlanCaseMedia {
  id: string;
  fileName: string;
  fileSize: number;
  mimeType: string;
  src: string;
}
export interface MediaCleanup {
  removed: string[];
  retained: string[];
  missing: string[];
}
const base = (planId: string) =>
  `/plan-orchestration/plans/${planId}/execution-media`;
export const planCaseMediaApi = {
  cleanup: (planId: string, ids: string[]) =>
    apiClient.post<MediaCleanup>(`${base(planId)}/cleanup`, { ids }),
  upload: (planId: string, file: File) => {
    const data = new FormData();
    data.append("file", file);
    return apiClient.post<PlanCaseMedia>(base(planId), data, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  download: async (planId: string, id: string) =>
    (
      await apiClient
        .getInstance()
        .get<Blob>(`${base(planId)}/${id}/download`, { responseType: "blob" })
    ).data,
  remove: (planId: string, id: string) =>
    apiClient.delete(`${base(planId)}/${id}`),
};
/** 图片节点只向明确的本机图片路由发送登录凭据。 */
export function privateImagePath(source: string): string | undefined {
  return /^\/api\/v1\/plan-orchestration\/plans\/[a-zA-Z0-9-]+\/execution-media\/[a-f0-9-]{36}\/preview$/.test(
    source,
  )
    ? source.slice("/api/v1".length)
    : undefined;
}
