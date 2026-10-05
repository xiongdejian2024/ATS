import { describe, it, expect } from "vitest";
import { planNativeWorkspaceFields, planNativeColumns } from "../planNativeWorkspaceFields";
const project = { id:"项目", name:"当前项目" };
const native = { protocols:["HTTP","TCP"], environments:[{id:"来源环境",name:"跨项目配置环境"}] };
describe("官方计划原生字段与实例语义",()=>{
  it("API工作区使用计划结果和执行人，环境协议采用真实列表元数据，候选主结果及参数变更不混入",()=>{
    const fields=planNativeWorkspaceFields(project,[{id:"测试集",name:"已关联测试集",count:2}], [{id:"执行人",name:"真实执行者"}],"api",native);
    expect(fields.map(f=>f.key)).toEqual(["id","name","collectionId","moduleId","projectId","protocol","priority","result","nativeState","bugCount","path","environmentName","tags","executorId","createdBy","createdAt","updatedBy","updatedAt"]);
    expect(fields.find(f=>f.key==="result")?.options).toContainEqual({label:"成功",value:"SUCCESS"});
    expect(fields.find(f=>f.key==="environmentName")?.options).toEqual([{label:"跨项目配置环境",value:"来源环境"}]);
    expect(fields.find(f=>f.key==="protocol")?.options).toEqual([{label:"HTTP",value:"HTTP"},{label:"TCP",value:"TCP"}]);
    expect(fields.some(f=>["lastReportStatus","apiChange","planIds","reviewResult"].includes(f.key))).toBe(false);
  });
  it("场景字段保留步骤数及场景文案，默认列/隐藏列与官方顺序和宽度对应",()=>{
    const fields=planNativeWorkspaceFields(project,[],[],"scenario",native);
    expect(fields.map(f=>f.key)).toEqual(["id","name","collectionId","moduleId","projectId","priority","nativeState","result","tags","bugCount","environmentName","stepTotal","executorId","createdBy","createdAt","updatedBy","updatedAt"]);
    expect(fields.find(f=>f.key==="name")?.label).toBe("场景名称");
    expect(fields.find(f=>f.key==="priority")?.label).toBe("场景等级");
    expect(fields.find(f=>f.key==="stepTotal")?.min).toBe(0);
    const api=planNativeColumns("api"),scene=planNativeColumns("scenario");
    expect(api.filter(c=>c.defaultVisible).map(c=>c.key)).toEqual(["caseCode","name","protocol","collectionName","createdAt","updatedAt","bugCount","priority","nativeResult","moduleName","projectName","createdByName","nativeExecutorName"]);
    expect(scene.filter(c=>c.defaultVisible).map(c=>c.key)).toEqual(["caseCode","name","collectionName","priority","nativeResult","createdAt","updatedAt","moduleName","bugCount","projectName","createdByName","nativeExecutorName"]);
    expect(api.filter(c=>!c.defaultVisible).map(c=>c.key)).toEqual(["nativeState","path","nativeExecutionEnvironmentName"]);
    expect(scene.find(c=>c.key==="nativeResult")?.width).toBe(200);
    expect(api.filter(c=>c.required).map(c=>c.key)).toEqual(["caseCode","name"]);
  });
});
