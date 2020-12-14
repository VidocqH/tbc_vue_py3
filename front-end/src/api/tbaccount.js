import request from '@/utils/request'
import store from '@/store/index'

export function getAccounts(params) {
  const user_id = (JSON.parse(atob(store.getters.token.split('.')[1]))).user_id
  return request({
    url: '/tbaccounts/' + user_id,
    method: 'get',
    params
  })
}

export function putAccounts(data) {
  const user_id = (JSON.parse(atob(store.getters.token.split('.')[1]))).user_id
  return request({
    url: '/tbaccounts/' + user_id,
    method: 'put',
    data
  })
}

export function delAccounts(data) {
  const user_id = (JSON.parse(atob(store.getters.token.split('.')[1]))).user_id
  return request({
    url: '/tbaccounts/' + user_id,
    method: 'delete',
    data
  })
}

export function addAccounts(data) {
  const user_id = (JSON.parse(atob(store.getters.token.split('.')[1]))).user_id
  return request({
    url: '/tbaccounts/' + user_id,
    method: 'post',
    data
  })
}

export function beginCollect(data) {
  return request({
    url: '/tbcollect/' + data.username,
    method: 'post',
    data
  })
}

export function stopCollect(account) {
  return request({
    url: '/tbcollect/' + account,
    method: 'delete'
  })
}
