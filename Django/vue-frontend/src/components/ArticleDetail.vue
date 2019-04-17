<template>
  <div>
    <h1>{{article.title}}</h1>
    <span class="update_time">{{article.modified_at}}</span>
    <vue-markdown>{{article.content}}</vue-markdown>
  </div>
</template>

<script>
    import VueMarkdown from 'vue-markdown'

    export default {
        props: ['id'],
        computed: {
            article () {
            return this.$store.getters.GetArticleById(this.id)
            }
        },
        components: {
            VueMarkdown
        }
    }
</script>

<style scoped>

</style>
