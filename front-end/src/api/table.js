import request from '@/utils/request'

export function getList(params) {
  return request({
    url: 'shops',
    method: 'get',
    params
  })
}
