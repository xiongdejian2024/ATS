import {isNavigationFailure,NavigationFailureType,type Router} from 'vue-router'
import {notificationApi} from '@/api/notification'
import type {Notification} from '@/types'

export async function openNotification(item:Notification,router:Router){
  if(item.type.startsWith('mention_')){
    await notificationApi.source(item.id)
    const failure=await router.push({name:'MentionSource',params:{notificationId:item.id}})
    if(isNavigationFailure(failure,NavigationFailureType.aborted|NavigationFailureType.cancelled))return false
  }
  await notificationApi.markAsRead(item.id)
  return true
}
