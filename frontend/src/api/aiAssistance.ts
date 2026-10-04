import { apiClient } from '@/utils/api'

export interface ModelConfiguration {
  base_url: string; model: string; api_key?: string; clear_api_key?: boolean
  has_api_key?: boolean; timeout_seconds: number; enabled: boolean
}
export interface DraftContent {
  name: string; type: string; priority: string; precondition: string
  requirement_ref: string; steps: { action: string; expected: string }[]; tags: string[]
}
export interface AIDraft {
  id: string; project_id: string; batch_id: string; content: DraftContent
  status: 'draft' | 'imported' | 'dismissed'; revision: number; imported_case_id?: string; created_at: string
}
export interface Conversation { id: string; title: string; messages: { role: string; content: string }[] }
export const aiApi = {
  configuration: () => apiClient.get<{ personal: ModelConfiguration | null; system: ModelConfiguration | null; can_manage_system: boolean }>('/ai/configuration'),
  saveConfiguration: (scope: string, body: ModelConfiguration) => apiClient.put<ModelConfiguration>(`/ai/configuration/${scope}`, body),
  removePersonal: () => apiClient.delete('/ai/configuration/personal'),
  test: () => apiClient.post('/ai/configuration/test', {}, { timeout: 190000 }),
  conversations: (project_id: string) => apiClient.get<{ id: string; title: string }[]>('/ai/conversations', { params: { project_id } }),
  conversation: (id: string) => apiClient.get<Conversation>(`/ai/conversations/${id}`),
  removeConversation: (id: string) => apiClient.delete(`/ai/conversations/${id}`),
  chat: (body: { project_id: string; message: string; conversation_id?: string }) => apiClient.post<Conversation>('/ai/chat', body, { timeout: 190000 }),
  generate: (body: { project_id: string; requirement: string; count: number; case_type: string }) => apiClient.post<AIDraft[]>('/ai/generate-cases', body, { timeout: 190000 }),
  drafts: (project_id: string) => apiClient.get<AIDraft[]>('/ai/drafts', { params: { project_id } }),
  updateDraft: (item: AIDraft) => apiClient.put<AIDraft>(`/ai/drafts/${item.id}`, { revision: item.revision, content: item.content }),
  accept: (item: AIDraft) => apiClient.post<AIDraft>(`/ai/drafts/${item.id}/accept`, { revision: item.revision }),
  dismiss: (item: AIDraft) => apiClient.post<AIDraft>(`/ai/drafts/${item.id}/dismiss`, { revision: item.revision }),
}
