import { apiClient } from "@/utils/api";

export interface HttpBody {
  base64: string;
  byteLength: number;
  capturedBytes: number;
  truncated: boolean;
  contentType: string;
  charset: string;
}
export interface HttpRequest {
  method: string;
  url: string;
  headers: [string, string][];
  headersTruncated?: boolean;
  body: HttpBody;
}
export interface HttpResponse {
  statusCode: number;
  reason: string;
  httpVersion: string;
  headers: [string, string][];
  headersTruncated?: boolean;
  body: HttpBody;
  responseTimeMs: number | null;
}
export interface HttpAssertion {
  name: string;
  assertionType: string;
  condition: string;
  expression: string;
  actualValue: string;
  expectedValue: string;
  actualTruncated: boolean;
  expectedTruncated: boolean;
  actualPresent: boolean;
  passed: boolean;
  message: string;
  groupId?: string;
  rowIndex?: number;
}
export interface HttpAttempt {
  attempt: number;
  result: string;
  duration: number;
  request?: HttpRequest;
  response?: HttpResponse;
  assertions: HttpAssertion[];
  error?: string;
  redirects: { request: HttpRequest; response: HttpResponse }[];
  console?: string[];
}
export interface HttpStep {
  index: number;
  name: string;
  method: string;
  result: string;
  duration: number;
  attempts: HttpAttempt[];
  error?: string;
}
export interface HttpDetail {
  version: 1;
  totalSteps: number;
  omittedSteps: number;
  steps: HttpStep[];
}
export interface NativeHttpReport {
  executionId: string;
  caseId: string;
  category: string;
  result: string;
  duration?: string;
  available: boolean;
  native?: boolean;
  message?: string;
  detail?: HttpDetail;
}
export const nativeHttpReportApi = {
  detail: (
    runId: string,
    executionId: string,
    caseId: string,
  ): Promise<NativeHttpReport> =>
    apiClient.get(
      `/plan-orchestration/runs/${runId}/native-cases/${executionId}/${caseId}/detail`,
    ),
};

export function bytes(body: HttpBody) {
  return Uint8Array.from(atob(body.base64), (c) => c.charCodeAt(0));
}
export function decodeBody(body: HttpBody, charset = body.charset || "utf-8") {
  return new TextDecoder(charset).decode(bytes(body));
}
export function assertionRows(
  rows: HttpAssertion[],
  status?: boolean,
  order?: "ascend" | "descend",
) {
  const result = rows.filter(
    (r) => status === undefined || r.passed === status,
  );
  return order
    ? result
        .slice()
        .sort(
          (a, b) =>
            (Number(a.passed) - Number(b.passed)) *
            (order === "ascend" ? 1 : -1),
        )
    : result;
}
