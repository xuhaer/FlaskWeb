<template>
  <div>
    <h1>VUEX</h1>
    <div v-for="artitle in artitle_list" >
      <h1>{{artitle.title}}</h1>
      <span class="update_time">{{artitle.modified_at}}</span>
      <p class="digest">{{artitle.digest}}</p>
      <router-link :to="{name: 'ArticleDetail', params: {id: artitle.id}}">阅读详情</router-link>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  data() {
    return {

    };
  },
  computed: {
    artitle_list() {
      return this.$store.state.blog.article_list
    }
  },
  beforeCreate() {
    this.$store.dispatch('ArticleInit');
  },
}
</script>

<style scoped>

</style>