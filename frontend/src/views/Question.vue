<template>
  <div class="single-question mt-2">
    <div class="container">
      <h1>
        {{ question.id }}
        {{ question.etc }}
      </h1>
      <p>
        <span>{{ question.author }}</span>
      </p>
      <p>{{ question.created_at }}</p>
    </div>
  </div>
</template>

<script>
import { apiService } from "../common/api.service.js";
export default {
  name: "Question",
  props: {
    id: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      question: {}
    };
  },
  methods: {
    getQuestionData() {
      let endpoint = `/api/questions/${this.id}/`;
      apiService(endpoint).then(data => {
        this.question = data;
      });
    }
  },
  created() {
    this.getQuestionData();
    console.log(this.question);
  }
};
</script>
