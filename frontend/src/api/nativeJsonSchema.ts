import { apiClient } from "@/utils/api";
import type { JsonSchema } from "@/components/TestCase/nativeJsonSchema";
export const convertJsonSchema = (
  project: string,
  schema: JsonSchema,
  action: "preview" | "generate",
) =>
  apiClient.post<{ jsonValue: string }>(
    `/projects/${project}/native-cases/json-schema/convert`,
    { jsonSchema: schema, action },
    { timeout: 60000 },
  );
