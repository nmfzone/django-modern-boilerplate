import $ from 'jquery'
import Axios from 'axios'
import Lodash from 'lodash'


window._ = Lodash

window.$ = window.jQuery = $

window.axios = Axios

window.axios.defaults.headers.common = {
  'X-CSRF-TOKEN': window.App.csrfToken,
  'X-Requested-With': 'XMLHttpRequest',
}
