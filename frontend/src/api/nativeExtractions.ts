import { apiClient } from "@/utils/api";
import type { Extractor } from "@/components/TestCase/nativeExtractions";
import type { HttpAttempt } from "./nativeHttpReport";
export interface ExtractionResponse {
  available: boolean;
  response: HttpAttempt | null;
  executionId: string | null;
  message: string;
}
const base = (project: string, id: string) =>
  `/projects/${project}/native-cases/cases/${id}`;
export const extractionApi = {
  response: (project: string, id: string): Promise<ExtractionResponse> =>
    apiClient.get(base(project, id) + "/extraction-response"),
  preview: (
    project: string,
    id: string,
    rule: Extractor,
    expectedExecutionId: string,
  ): Promise<{ values: string[]; executionId: string }> =>
    apiClient.post(base(project, id) + "/extraction-preview", {
      ...rule,
      expectedExecutionId,
    }),
};
