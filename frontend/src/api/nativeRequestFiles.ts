import { apiClient } from "@/utils/api";
export interface RequestFile {
  fileId: string;
  fileName: string;
  byteLength: number;
  contentType: string;
  sha256: string;
}
export interface FileReference {
  fileId: string;
  fileAlias?: string;
}
const base = (project: string) =>
  `/projects/${project}/native-cases/request-files`;
export const nativeRequestFilesApi = {
  list: (
    project: string,
    params: { page: number; size: number; search: string },
  ) =>
    apiClient.get<{ items: RequestFile[]; total: number; maxFileSize: number }>(
      base(project),
      { params },
    ),
  metadata: (project: string, id: string) =>
    apiClient.get<RequestFile>(base(project) + "/" + id),
  upload: (project: string, file: File) => {
    const form = new FormData();
    form.append("file", file);
    return apiClient.post<RequestFile>(base(project), form, {
      headers: { "Content-Type": "multipart/form-data" },
      timeout: 60000,
    });
  },
  remove: (project: string, id: string) =>
    apiClient.delete(base(project) + "/" + id),
  download: async (project: string, id: string) =>
    (
      await apiClient
        .getInstance()
        .get<Blob>(base(project) + "/" + id + "/download", {
          responseType: "blob",
          timeout: 60000,
        })
    ).data,
};
