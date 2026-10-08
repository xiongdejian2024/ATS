export interface FrozenTestSet {
  id: string | null;
  name: string;
  path: { id: string; name: string }[];
}
export interface FrozenPolicy {
  key: string;
  planRunId?: string;
  planName?: string;
  executionMode?: "serial" | "parallel";
  stopOnFailure?: boolean;
  passThreshold?: number;
  extended?: boolean;
  retryOnFailure?: boolean;
  retryTimes?: number;
  retryInterval?: number;
  testResourcePoolId?: string;
  requestEnvironmentId?: string;
  requestEnvironmentGroupId?: string;
  resolvedRequestEnvironmentId?: string;
  requestEnvironmentGroupRevision?: number;
}
export interface FrozenOccurrence {
  key: string;
  planRunId: string;
  planName: string;
  caseId: string;
  caseName: string;
  associationId: string;
  executionId?: string;
  category: string;
  testSet: FrozenTestSet;
  stepIndex: number;
  title: string;
  status?: string;
}
export interface ReportDetails {
  testSets: {
    key: string;
    planRunId: string;
    planName: string;
    category: string;
    testSet: FrozenTestSet;
    total: number;
    counts: Record<string, number>;
    defectCount: number;
    passRate: number;
  }[];
  defects: {
    id: string;
    title: string;
    status?: string;
    occurrenceCount: number;
    occurrences: FrozenOccurrence[];
  }[];
  configuration: {
    policies: FrozenPolicy[];
    items: {
      id: string;
      planRunId: string;
      planName: string;
      suiteName: string;
      category: string;
      testSet: FrozenTestSet;
      executionId: string;
      environmentId?: string;
      resourcePool: string[];
      executionConfig: Omit<FrozenPolicy, "key">;
    }[];
  };
}
