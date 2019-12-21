<template>
  <div class="container mt-2">
    <h1 class="mb-3">최고의 제안하기</h1>
    <form @submit.prevent="onSubmit">
      <textarea
        v-model="answerBody"
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
  name: "AnswerEditor",
  props: {
    id: {
      type: [Number, String],
      required: true
    }
    // previousAnswer: {
    //   type: String,
    //   required: true
    // },
    // questionId: {
    //   type: Number,
    //   required: true
    // }
  },
  data() {
    return {
      answerBody: this.previousAnswer,
      error: null
    };
  },
  methods: {
    onSubmit() {
      if (this.answerBody) {
        let endpoint = `/api/answers/${this.id}/`;
        apiService(endpoint, "PUT", { body: this.answerBody }).then(() => {
          this.$router.push({
            name: "question",
            params: { id: this.questionId }
          });
        });
      } else {
        this.error = "You can't submit an empty answer!";
      }
    }
  },
  async beforeRouteEnter(to, from, next) {
    let endpoint = `/api/answers/${to.params.id}/`;
    let data = await apiService(endpoint);
    // to.params.previousAnswer = data.body;
    // to.params.questionId= data.question_id;
    return next(vm => ((vm.answerBody = data.body), (vm.questionId = data.question_id)));
  }
};
</script>
