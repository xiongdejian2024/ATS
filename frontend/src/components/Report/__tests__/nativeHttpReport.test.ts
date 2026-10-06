import { describe, expect, it } from "vitest";
import {
  assertionRows,
  bytes,
  decodeBody,
  type HttpAssertion,
  type HttpBody,
} from "@/api/nativeHttpReport";
function capture(value: Uint8Array, charset = "utf-8"): HttpBody {
  return {
    base64: btoa(String.fromCharCode(...value)),
    byteLength: value.length,
    capturedBytes: value.length,
    truncated: false,
    charset,
    contentType: "text/plain",
  };
}
describe("HTTP实际报告数据", () => {
  it("正文按实际字节与字符集解码，不把HTML当成DOM", () => {
    const body = capture(
      new TextEncoder().encode("实际响应<script>alert(1)</script>"),
    );
    expect(decodeBody(body)).toBe("实际响应<script>alert(1)</script>");
    expect(bytes(body)).toEqual(
      new TextEncoder().encode("实际响应<script>alert(1)</script>"),
    );
    expect(
      decodeBody(capture(Uint8Array.from([0x41, 0, 0x42, 0]), "utf-16le")),
    ).toBe("AB");
  });
  it("断言按真实结果筛选和排序，不修改冻结原列表", () => {
    const rows = [
      { name: "first", passed: true },
      { name: "second", passed: false },
      { name: "third", passed: true },
    ] as HttpAssertion[];
    expect(assertionRows(rows, false).map((r) => r.name)).toEqual(["second"]);
    expect(assertionRows(rows, undefined, "ascend").map((r) => r.name)).toEqual(
      ["second", "first", "third"],
    );
    expect(rows.map((r) => r.name)).toEqual(["first", "second", "third"]);
  });
  it("缺少或非法字符集报出真实解码异常，仍可取得原始字节", () => {
    const body = capture(Uint8Array.from([255, 0, 1]), "not-a-charset");
    expect(() => decodeBody(body)).toThrow();
    expect(bytes(body)).toEqual(Uint8Array.from([255, 0, 1]));
  });
});
