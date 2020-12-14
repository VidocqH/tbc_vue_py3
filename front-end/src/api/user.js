import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/tokens',
    method: 'post',
    headers: ({
      Authorization: JSON.stringify(
        'Basic ' + btoa(data.username + ':' + data.password)
      )
    })
  })
}

export function getInfo(token) {
  const user_id = (JSON.parse(atob(token.split('.')[1]))).user_id
  return request({
    url: '/users/' + user_id,
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/users/logout',
    method: 'post'
  })
}

export function register(data) {
  return request({
    url: '/users',
    method: 'post',
    data
  })
}
