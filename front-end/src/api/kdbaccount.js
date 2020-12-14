import request from '@/utils/request'
import store from '@/store/index'

export function getKdbAccounts(params) {
  const user_id = (JSON.parse(atob(store.getters.token.split('.')[1]))).user_id
  return request({
    url: '/kdbaccounts/' + user_id,
    method: 'get',
    params
  })
}

export function putKdbAccounts(data) {
  const user_id = (JSON.parse(atob(store.getters.token.split('.')[1]))).user_id
  return request({
    url: '/kdbaccounts/' + user_id,
    method: 'put',
    data
  })
}

export function delKdbAccounts(data) {
  const user_id = (JSON.parse(atob(store.getters.token.split('.')[1]))).user_id
  return request({
    url: '/kdbaccounts/' + user_id,
    method: 'delete',
    data
  })
}

export function addKdbAccounts(data) {
  const user_id = (JSON.parse(atob(store.getters.token.split('.')[1]))).user_id
  return request({
    url: '/kdbaccounts/' + user_id,
    method: 'post',
    data
  })
}

export function beginKdbCollect(account) {
  return request({
    url: '/kdbcollect/' + account,
    method: 'post'
  })
}

export function stopKdbCollect(account) {
  return request({
    url: '/kdbcollect/' + account,
    method: 'delete'
  })
}
