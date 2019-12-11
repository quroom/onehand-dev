<template>
  <div class="container mt-2">
    <h1 class="mb-3">일괄 요청서 작성</h1>
    <form @submit.prevent="onSubmit">
      <textarea
        v-model="question_etc"
        class="form-control"
        placeholder="기타 요청사항"
        rows="3"
      ></textarea>
      <button type="submit" class="btn btn-success">제출</button>
    </form>
  </div>
</template>
<script>
import { apiService } from "../common/api.service.js";

export default {
  name: "QuestionEditor",
  props: {  
  },
  data() {
    return {
      question_etc: null,
      question_end_date: null,
      question_moving_date: null,
      question_item_category: null,
      question_trade_category: null,
      error: null
    };
  },
  methods: {
    onSubmit() {
      if (!this.question_etc) {
        this.question_etc = "빔"
      } else {
        let endpoint = "/api/questions/";
        let method = "POST";
        if (this.id !== undefined) {
          endpoint += `${ this.id }/`;
          method = "PUT";
        }
        console.log(this)
        apiService(endpoint, method, { 
          etc: this.question_etc,
          end_date: "2019-11-02",
          moving_date: "2021-11-11",
          trade_category : [1],
          item_category : [1]
          }).then(
          question_data => {
            this.$router.push({
              name: "question",
              params: { id: question_data.id }
            });
          }
        );
      }      
    }
  },
  async beforeRouteEnter(to, from, next) {
    if (to.params.id !== undefined) {
      let endpoint = `/api/questions/${ to.params.id }/`;
      // this.id = to.params.id;
      let data = await apiService(endpoint);
      return next(vm => (
        vm.question_etc = data.etc,
        vm.id = data.id))
    } else {
      return next();
    }
  },
  created() {
    document.title = "원페이퍼 작성하기";
  }
};
</script>
