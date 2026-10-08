import {apiClient} from '@/utils/api'
export interface MentionMember {id:string;label:string;username:string}
export const mentionsApi={
  members:(projectId:string,params:{context:'case'|'plan';search:string;page:number})=>apiClient.get<{items:MentionMember[];total:number;page:number;size:number}>(`/projects/${projectId}/mention-members?${new URLSearchParams({context:params.context,search:params.search,page:String(params.page)})}`),
}
