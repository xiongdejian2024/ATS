import {apiClient} from '@/utils/api'
export interface LibraryFile {id:string;folderId?:string;fileName:string;fileSize:number;mimeType:string;sha256:string;src?:string;archived:boolean;published:boolean;uploadedBy:string;createdAt:string}
export interface LibraryFolder {id:string;name:string;parentId?:string}
const base=(projectId:string)=>`/projects/${projectId}/file-library`
export const fileLibraryApi={
 folders:(p:string)=>apiClient.get<LibraryFolder[]>(`${base(p)}/folders`),
 saveFolder:(p:string,body:{name:string;parentId?:string},id?:string)=>id?apiClient.put<LibraryFolder>(`${base(p)}/folders/${id}`,body):apiClient.post<LibraryFolder>(`${base(p)}/folders`,body),
 files:(p:string,params:{folderId?:string;search?:string;page?:number;archived?:boolean;imagesOnly?:boolean})=>apiClient.get<{items:LibraryFile[];total:number;page:number;size:number;canManage:boolean}>(`${base(p)}/files`,{params}),
 upload:(p:string,file:File,options:{folderId?:string;image?:boolean;published?:boolean}={})=>{const form=new FormData();form.append('file',file);if(options.folderId)form.append('folderId',options.folderId);form.append('image',String(!!options.image));form.append('published',String(!!options.published));return apiClient.post<LibraryFile>(`${base(p)}/files`,form,{headers:{'Content-Type':'multipart/form-data'}})},
 download:async(p:string,id:string)=>(await apiClient.getInstance().get<Blob>(`${base(p)}/files/${id}/download`,{responseType:'blob'})).data,
 archive:(p:string,id:string,archived:boolean)=>apiClient.put(`${base(p)}/files/${id}/archive`,{archived}),
 references:(p:string,id:string)=>apiClient.get<LibraryFile[]>(`${base(p)}/cases/${id}/references`),
 associate:(p:string,id:string,fileIds:string[])=>apiClient.post<LibraryFile[]>(`${base(p)}/cases/${id}/references`,{fileIds}),
 unlink:(p:string,id:string,fileId:string)=>apiClient.delete(`${base(p)}/cases/${id}/references/${fileId}`),
}
