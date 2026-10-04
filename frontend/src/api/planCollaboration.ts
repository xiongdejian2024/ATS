import { apiClient } from '@/utils/api'
import {useUserStore} from '@/stores/user'
import type {PlanRun,RunCase} from './planOrchestration'
export interface StepResult {index:number;result:string;actual:string;notes:string;defectIds:string[];attachments:string[]}
export interface ReportCase extends RunCase {associationId?:string;category?:string;snapshot?:{precondition?:string;steps?:{action?:string;expected?:string}[]};stepResults?:StepResult[];linkedAutomation?:boolean;assignedTo?:string}
export type ReportRun=PlanRun & {summary?:{conclusion?:string;risk?:string;notes?:string};report:PlanRun['report'] & {categories?:Record<string,{total:number;counts:Record<string,number>}>;cases:ReportCase[]}}
const base='/plan-orchestration'
export const planCollaborationApi={
 report:(id:string):Promise<ReportRun>=>apiClient.get(`${base}/runs/${id}/report`),
 summary:(id:string,data:Record<string,string>)=>apiClient.put(`${base}/runs/${id}/summary`,data),
 collaboration:(id:string,associationId:string):Promise<{comments:{id:string;content:string;authorId:string;createdAt:string}[];attachments:{id:string;name:string}[]}>=>apiClient.get(`${base}/runs/${id}/cases/${associationId}/collaboration`),
 comment:(id:string,associationId:string,content:string)=>apiClient.post(`${base}/runs/${id}/cases/${associationId}/comments`,{content}),
 attachment:(id:string,associationId:string,data:{name:string;contentBase64:string;mimeType:string})=>apiClient.post<{id:string;name:string}>(`${base}/runs/${id}/cases/${associationId}/attachments`,data),
 result:(id:string,associationId:string,data:{result:string;notes:string;stepResults:StepResult[]})=>apiClient.put(`${base}/runs/${id}/cases/${associationId}/result`,data),
 share:(id:string,expiresHours:number)=>apiClient.post<{id:string;path:string;expiresAt:string}>(`${base}/runs/${id}/shares`,{expiresHours}),
 shares:(id:string)=>apiClient.get<{id:string;expiresAt:string;revoked:boolean}[]>(`${base}/runs/${id}/shares`),
 revoke:(id:string)=>apiClient.delete(`${base}/shares/${id}`)
}
export async function downloadPlanFile(path:string,name:string){const token=useUserStore().accessToken || localStorage.getItem('access_token');const response=await fetch(`/api/v1/plan-orchestration/${path}`,{headers:{Authorization:`Bearer ${token}`}});if(!response.ok)throw new Error(`文件下载失败：${response.status}`);const blob=await response.blob();const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}
