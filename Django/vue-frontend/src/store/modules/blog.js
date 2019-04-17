// import router from '../../router'
import axios from 'axios'

const ARTICLE_INIT = 'ARTICLE_INIT'

export default {
  state: {
    article_list: [],
    comment_list: []
  },
  mutations: {
    [ARTICLE_INIT] (state, data) {
      state.article_list = data
    }
  },
  actions: {
    ArticleInit ({commit}) {
      // 页面加载时获取数据
      axios.get('http://127.0.0.1:8000/api/article/')
        .then(response => {
          console.log('成功获取数据')
          commit(ARTICLE_INIT, response.data)
        })
        .catch(error => {
          alert('获取数据错误:', error)
        })
    }
  },
  getters: {
    GetArticleById: state => (id) => {
      // 因 vuex-persist 会把 id 转为 string 类型
      return state.article_list.find(article => article.id === parseInt(id))
    }
  }
}
