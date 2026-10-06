<template>
  <div class="native-http-report">
    <a-alert
      v-if="!report.available"
      type="info"
      :message="report.message || '此执行没有HTTP交换详情'"
    />
    <template v-else-if="report.detail">
      <a-alert
        v-if="report.detail.omittedSteps"
        type="warning"
        :message="`本次详情捕获${report.detail.steps.length}/${report.detail.totalSteps}步骤，超出捕获范围的${report.detail.omittedSteps}步骤未保存详情`"
      />
      <div class="http-report-layout">
        <div class="http-step-nav" aria-label="实际HTTP请求步骤">
          <button
            v-for="row in report.detail.steps"
            :key="row.index"
            class="http-step"
            :class="{ active: row.index === stepIndex }"
            @click="select(row.index)"
          >
            <span>{{ row.index + 1 }} {{ row.name }}</span
            ><a-tag :color="statusColor(row.result)">{{
              label(row.result)
            }}</a-tag
            ><small>{{ row.method }} · {{ ms(row.duration) }} ms</small>
          </button>
        </div>
        <div v-if="step" class="http-step-result">
          <a-space wrap class="http-summary"
            ><strong>{{ step.name }}</strong
            ><a-tag :color="statusColor(step.result)">{{
              label(step.result)
            }}</a-tag
            ><span>耗时 {{ ms(step.duration) }} ms</span></a-space
          >
          <a-radio-group
            v-if="step.attempts.length > 1"
            v-model:value="attemptIndex"
            aria-label="HTTP重试详情"
            class="attempts"
            ><a-radio-button
              v-for="(row, index) in step.attempts"
              :key="row.attempt"
              :value="index"
              >{{ index === 0 ? "初次请求" : `失败重试${index}` }} ·
              {{ label(row.result) }}</a-radio-button
            ></a-radio-group
          >
          <a-alert
            v-if="step.error && !attempt"
            type="info"
            :message="step.error"
          />
          <template v-if="attempt">
            <a-alert
              v-if="attempt.error"
              type="error"
              :message="attempt.error"
            />
            <a-space v-if="attempt.redirects.length" wrap class="sub-requests"
              ><a-select
                v-model:value="subIndex"
                aria-label="响应内容或子请求"
                :options="[
                  { value: -1, label: '响应内容' },
                  ...attempt.redirects.map((r, i) => ({
                    value: i,
                    label: `子请求${i + 1} · ${r.response.statusCode}`,
                  })),
                ]"
                style="width: 220px"
            /></a-space>
            <a-space
              v-if="response"
              wrap
              class="http-response-summary"
              aria-label="实际HTTP响应概要"
              ><a-tag :color="response.statusCode < 400 ? 'green' : 'red'"
                >{{ response.statusCode }} {{ response.reason }}</a-tag
              ><span>{{
                response.responseTimeMs === null
                  ? "耗时未单独记录"
                  : `${response.responseTimeMs.toFixed(3)} ms`
              }}</span
              ><span>{{ response.body.byteLength }} bytes</span
              ><span>{{ response.httpVersion }}</span></a-space
            >
            <a-tabs v-model:active-key="tab">
              <a-tab-pane key="body" tab="响应内容"
                ><HttpResultBody
                  v-if="response"
                  :body="response.body" /><a-empty
                  v-else
                  description="请求未取得响应内容"
              /></a-tab-pane>
              <a-tab-pane key="headers" tab="响应头"
                ><a-alert
                  v-if="response?.headersTruncated"
                  type="warning"
                  message="响应头超过捕获范围，下面只包含已捕获头部" /><a-table
                  v-if="response"
                  :data-source="pairs(response.headers)"
                  :columns="headerColumns"
                  :pagination="false"
                  size="small"
                  :scroll="{ x: 500 }"
                  row-key="index" /><a-empty
                  v-else
                  description="请求未取得响应头"
              /></a-tab-pane>
              <a-tab-pane key="request" tab="实际请求"
                ><template v-if="request"
                  ><a-alert
                    v-if="request.headersTruncated"
                    type="warning"
                    message="请求头超过捕获范围，下面只包含已捕获头部" />
                  <p class="actual-url">
                    <a-tag>{{ request.method }}</a-tag
                    >{{ request.url }}
                  </p>
                  <a-table
                    :data-source="pairs(request.headers)"
                    :columns="headerColumns"
                    :pagination="false"
                    size="small"
                    :scroll="{ x: 500 }"
                    row-key="index" />
                  <h4>请求正文</h4>
                  <HttpResultBody :body="request.body" /></template
                ><a-empty v-else description="此步骤未发送HTTP请求"
              /></a-tab-pane>
              <a-tab-pane
                key="assertions"
                :tab="`断言 (${attempt.assertions.length})`"
                ><a-space wrap class="assertion-filter"
                  ><span>状态</span
                  ><a-select
                    v-model:value="assertionStatus"
                    allow-clear
                    aria-label="断言结果筛选"
                    placeholder="全部"
                    :options="[
                      { value: 'true', label: '成功' },
                      { value: 'false', label: '失败' },
                    ]"
                    style="width: 120px" /></a-space
                ><a-table
                  :data-source="filteredAssertions"
                  :columns="assertionColumns"
                  :pagination="false"
                  size="small"
                  :scroll="{ x: 1060 }"
                  :row-key="assertionKey"
                  @change="sortAssertions"
                  ><template #bodyCell="{ column, record }"
                    ><template v-if="column.key === 'name'"
                      >【{{ kind(record.assertionType) }}】{{
                        record.name
                      }}</template
                    ><template v-else-if="column.key === 'condition'">{{
                      condition(record.condition)
                    }}</template
                    ><template v-else-if="column.key === 'passed'"
                      ><a-tag :color="record.passed ? 'green' : 'red'">{{
                        record.passed ? "成功" : "失败"
                      }}</a-tag></template
                    ><template v-else-if="column.key === 'actualValue'"
                      >{{
                        record.actualPresent
                          ? record.actualValue
                          : "未取得实际值"
                      }}<small v-if="record.actualTruncated"
                        >（已截断）</small
                      ></template
                    ><template v-else-if="column.key === 'expectedValue'"
                      >{{ record.expectedValue
                      }}<small v-if="record.expectedTruncated"
                        >（已截断）</small
                      ></template
                    ></template
                  ></a-table
                ></a-tab-pane
              >
              <a-tab-pane
                key="extract"
                :tab="`提取结果 (${attempt.extractResults?.length || 0})`"
                ><a-table
                  :data-source="attempt.extractResults || []"
                  :columns="extractColumns"
                  :pagination="false"
                  size="small"
                  :scroll="{ x: 880 }"
                  :row-key="(r: any) => r.processorId + ':' + r.extractorId"
                  ><template #bodyCell="{ column, record }"
                    ><template v-if="column.key === 'type'">{{
                      record.type === "TEMPORARY" ? "临时参数" : record.type
                    }}</template
                    ><template v-else-if="column.key === 'value'"
                      >{{ record.value
                      }}<small v-if="record.truncated"
                        >（已截断）</small
                      ></template
                    ><template v-else-if="column.key === 'message'"
                      ><a-tag :color="record.matched ? 'green' : 'orange'">{{
                        record.message
                      }}</a-tag></template
                    ></template
                  ></a-table
                ></a-tab-pane
              >
              <a-tab-pane key="console" tab="控制台">
                <pre class="http-console">{{
                  attempt.console?.join("\n") || "此执行没有额外控制台输出"
                }}</pre>
              </a-tab-pane>
            </a-tabs>
          </template>
        </div>
      </div>
    </template>
  </div>
</template>
<script setup lang="ts">
import { computed, ref, watch } from "vue";
import type { TableProps } from "ant-design-vue";
import {
  assertionRows,
  type NativeHttpReport,
  type HttpAssertion,
} from "@/api/nativeHttpReport";
import {
  conditions,
  responseKinds,
} from "@/components/TestCase/nativeResponseAssertions";
import HttpResultBody from "./HttpResultBody.vue";
const props = defineProps<{ report: NativeHttpReport }>();
const stepIndex = ref(0),
  attemptIndex = ref(0),
  subIndex = ref(-1),
  tab = ref("body"),
  assertionStatus = ref<string>(),
  assertionOrder = ref<"ascend" | "descend">();
const step = computed(() =>
    props.report.detail?.steps.find((s) => s.index === stepIndex.value),
  ),
  attempt = computed(() => step.value?.attempts[attemptIndex.value]);
const selected = computed(() =>
  subIndex.value >= 0
    ? attempt.value?.redirects[subIndex.value]
    : attempt.value,
);
const request = computed(() => selected.value?.request),
  response = computed(() => selected.value?.response);
const ms = (value: number) => (value * 1000).toFixed(3),
  label = (value: string) =>
    ({ passed: "成功", failed: "失败", error: "错误", skipped: "跳过" })[
      value
    ] || value,
  statusColor = (value: string) =>
    value === "passed" ? "green" : value === "skipped" ? "default" : "red";
const kind = (value: string) =>
  responseKinds.find((k) => k.value === value)?.label ||
  { status: "状态码", header: "响应头", json: "JSON", text: "响应体" }[value] ||
  value;
const condition = (value: string) =>
  conditions.find((c) => c.value === value)?.label ||
  {
    equals: "等于",
    not_equals: "不等于",
    contains: "包含",
    exists: "存在",
    not_exists: "不存在",
    XPATH: "XPath",
    REGEX: "正则匹配",
  }[value] ||
  value;
const extractColumns = [
  { title: "参数名", dataIndex: "name", width: 150 },
  { title: "提取值", key: "value", width: 200 },
  { title: "类型", key: "type", width: 120 },
  { title: "表达式", dataIndex: "expression", width: 200 },
  { title: "结果", key: "message", width: 210 },
];
const headerColumns = [
  { title: "参数名", dataIndex: "name", width: 180 },
  { title: "参数值", dataIndex: "value" },
];
const assertionColumns = [
  { title: "断言项", key: "name", width: 200 },
  { title: "实际值", key: "actualValue", width: 200 },
  { title: "匹配条件", key: "condition", width: 120 },
  { title: "预期值", key: "expectedValue", width: 200 },
  { title: "状态", key: "passed", sorter: true, width: 100 },
  { title: "原因", dataIndex: "message", width: 240 },
];
const assertionKey = (row: HttpAssertion, index?: number) =>
  `${row.groupId || row.assertionType}:${row.rowIndex ?? index}:${row.name}`;
const pairs = (rows: [string, string][]) =>
  rows.map(([name, value], index) => ({ index, name, value }));
const filteredAssertions = computed(() =>
  assertionRows(
    attempt.value?.assertions || [],
    assertionStatus.value === undefined
      ? undefined
      : assertionStatus.value === "true",
    assertionOrder.value,
  ),
);
const sortAssertions: NonNullable<TableProps["onChange"]> = (
  _page,
  _filter,
  sorter,
) => {
  const value = Array.isArray(sorter) ? sorter[0] : sorter;
  assertionOrder.value = value.order || undefined;
};
function select(index: number) {
  stepIndex.value = index;
  attemptIndex.value = 0;
  subIndex.value = -1;
  assertionStatus.value = undefined;
  assertionOrder.value = undefined;
}
watch(attemptIndex, () => {
  subIndex.value = -1;
  assertionStatus.value = undefined;
  assertionOrder.value = undefined;
});
watch(
  () => props.report.executionId + ":" + props.report.caseId,
  () => select(props.report.detail?.steps[0]?.index || 0),
  { immediate: true },
);
</script>
<style scoped>
.native-http-report {
  margin: 16px 0;
}
.http-report-layout {
  display: flex;
  gap: 12px;
  min-width: 0;
}
.http-step-nav {
  width: 216px;
  flex-shrink: 0;
  max-height: 620px;
  overflow: auto;
  background: #f7f8fa;
  padding: 8px;
}
.http-step {
  width: 100%;
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  padding: 10px;
  text-align: left;
  border: 1px solid transparent;
  background: none;
  cursor: pointer;
}
.http-step.active {
  background: white;
  border-color: #e5e6eb;
}
.http-step > span:first-child {
  width: 100%;
  overflow-wrap: anywhere;
}
.http-step-result {
  flex: 1;
  min-width: 0;
}
.http-summary,
.http-response-summary,
.attempts,
.sub-requests {
  margin-bottom: 12px;
}
.actual-url {
  overflow-wrap: anywhere;
}
.assertion-filter {
  margin-bottom: 10px;
}
.http-console {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  background: #f7f8fa;
  padding: 12px;
  max-height: 440px;
  overflow: auto;
}
@media (max-width: 650px) {
  .http-report-layout {
    flex-direction: column;
  }
  .http-step-nav {
    width: 100%;
    max-height: 220px;
  }
}
</style>
