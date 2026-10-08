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
  source?: 'http'|'mock';
  timings?: Partial<Record<'preparationMs'|'httpMs'|'extractionMs'|'assertionMs'|'preProcessorsMs'|'postProcessorsMs',number|null>>;
  processorResults?: {id:string;name:string;type:'sql'|'script';phase:string;result:string;durationMs:number;error?:string|null;rowCount?:number|null;bindings:{name:string;value:string;truncated:boolean}[]}[]|null;
  attempt: number;
  result: string;
  duration: number;
  request?: HttpRequest;
  response?: HttpResponse;
  assertions: HttpAssertion[];
  error?: string;
  redirects: { request: HttpRequest; response: HttpResponse }[];
  console?: string[];
  extractResults?: {
    name: string;
    value: string;
    type: string;
    expression: string;
    processorId: string;
    extractorId: string;
    matched: boolean;
    matchCount: number;
    truncated: boolean;
    message: string;
  }[];
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
  version: 1 | 2;
  globalProcessorResults?: NonNullable<HttpAttempt['processorResults']>;
  omittedGlobalProcessors?: number;
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
export function phaseTimings(attempt: HttpAttempt) {
  return (['preparationMs','httpMs','extractionMs','assertionMs','preProcessorsMs','postProcessorsMs'] as const).map(key=>({key,name:({preparationMs:'准备',httpMs:attempt.source==='mock'?'Mock响应':'HTTP交换',extractionMs:'参数提取',assertionMs:'断言',preProcessorsMs:'前置处理器',postProcessorsMs:'后置处理器'})[key],value: typeof attempt.timings?.[key]==='number' ? `${attempt.timings[key]!.toFixed(3)} ms` : '未记录'}));
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
