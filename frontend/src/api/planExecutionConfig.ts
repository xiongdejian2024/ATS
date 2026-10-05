import { apiClient } from "@/utils/api";
export interface ExecutionConfig {
  extended: boolean;
  executionMode: "serial" | "parallel";
  testResourcePoolId: string;
  requestEnvironmentId: string;
  stopOnFailure: boolean;
  retryOnFailure: boolean;
  retryTimes: number;
  retryInterval: number;
}
export interface ConfigurationEntry {
  scope: string;
  revision: number;
  config: ExecutionConfig;
  effectiveConfig: ExecutionConfig;
}
export interface ExecutionCatalog {
  configurations: Record<string, ConfigurationEntry>;
  pools: {
    id: string;
    name: string;
    environmentIds: string[];
    revision: number;
  }[];
  requestEnvironments: { id: string; name: string }[];
  resources: { id: string; name: string; enabled: boolean }[];
}
const base = (planId: string) => `/plan-orchestration/plans/${planId}`;
export const planExecutionApi = {
  catalog: (planId: string): Promise<ExecutionCatalog> =>
    apiClient.get(`${base(planId)}/execution-configurations`),
  save: (
    planId: string,
    scope: string,
    data: {
      config: ExecutionConfig;
      expectedRevision: number;
      name?: string;
      expectedName?: string;
    },
  ): Promise<ExecutionCatalog> =>
    apiClient.put(`${base(planId)}/execution-configurations/${scope}`, data),
  savePool: (
    planId: string,
    data: { name: string; environmentIds: string[]; expectedRevision: number },
    poolId?: string,
  ): Promise<ExecutionCatalog> =>
    poolId
      ? apiClient.put(`${base(planId)}/resource-pools/${poolId}`, data)
      : apiClient.post(`${base(planId)}/resource-pools`, data),
};
