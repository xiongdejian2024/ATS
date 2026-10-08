import { apiClient } from '@/utils/api'
import type { Notification, PaginationResponse } from '@/types'
import type {RouteLocationRaw} from 'vue-router'
export interface MentionSource {content:string;contentFormat:'plain'|'rich';sourceId:string;kind:string;createdAt:string;route:RouteLocationRaw}

export const notificationApi = {
  source:(notificationId:string)=>apiClient.get<MentionSource>(`/notifications/${notificationId}/source`),
  getNotifications: async (params?: {
    page?: number
    size?: number
    isRead?: boolean
    type?: string
  }): Promise<PaginationResponse<Notification>> => {
    const queryParams = new URLSearchParams()
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, String(value))
        }
      })
    }
    const url = `/notifications${queryParams.toString() ? '?' + queryParams.toString() : ''}`
    return apiClient.get(url)
  },

  markAsRead: async (notificationId: string): Promise<void> => {
    return apiClient.put(`/notifications/${notificationId}/read`)
  },

  markAllAsRead: async (): Promise<void> => {
    return apiClient.put('/notifications/read-all')
  },

  deleteNotification: async (notificationId: string): Promise<void> => {
    return apiClient.delete(`/notifications/${notificationId}`)
  }
}

