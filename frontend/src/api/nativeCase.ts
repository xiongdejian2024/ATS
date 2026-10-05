import { apiClient } from "@/utils/api";
export interface NativeDefinition {
  id: string;
  name: string;
  protocol: string;
  path: string;
  parameters: Record<string, unknown>;
  revision: number;
}
export interface NativeEnvironment {
  id: string;
  name: string;
  address: string;
  revision: number;
}
export interface NativeCatalog {
  definitions: NativeDefinition[];
  environments: NativeEnvironment[];
  protocols: string[];
  canCreate: boolean;
  canEdit: boolean;
}
export interface NativeFilterCatalog {
  protocols: string[];
  environments: { id: string; name: string }[];
}
export interface NativeConfig {
  lastReportStatus: string | null;
  stepTotal: number | null;
  state: string | null;
  apiDefinitionId: string | null;
  environmentId: string | null;
  parameters: Record<string, unknown>;
  revision: number;
  apiChange: boolean | null;
  canEdit: boolean;
}
const base = (project: string) => `/projects/${project}/native-cases`;
export const nativeCaseApi = {
  catalog: (project: string) =>
    apiClient.get<NativeCatalog>(base(project) + "/catalog"),
  config: (project: string, id: string) =>
    apiClient.get<NativeConfig>(base(project) + "/cases/" + id),
  saveConfig: (project: string, id: string, body: Record<string, unknown>) =>
    apiClient.put<NativeConfig>(base(project) + "/cases/" + id, body),
  saveDefinition: (
    project: string,
    body: Record<string, unknown>,
    id?: string,
  ) =>
    id
      ? apiClient.put<NativeCatalog>(base(project) + "/definitions/" + id, body)
      : apiClient.post<NativeCatalog>(base(project) + "/definitions", body),
  saveEnvironment: (
    project: string,
    body: Record<string, unknown>,
    id?: string,
  ) =>
    id
      ? apiClient.put<NativeCatalog>(
          base(project) + "/environments/" + id,
          body,
        )
      : apiClient.post<NativeCatalog>(base(project) + "/environments", body),
};
export const nativeStateOptions = (category: string) =>
  category === "api"
    ? [
        { label: "进行中", value: "PROCESSING" },
        { label: "已废弃", value: "DEPRECATED" },
        { label: "已完成", value: "DONE" },
      ]
    : [
        { label: "进行中", value: "UNDERWAY" },
        { label: "已废弃", value: "DEPRECATED" },
        { label: "已完成", value: "COMPLETED" },
      ];
export const nativeReportOptions = [
  { label: "成功", value: "SUCCESS" },
  { label: "失败", value: "ERROR" },
  { label: "误报", value: "FAKE_ERROR" },
];
