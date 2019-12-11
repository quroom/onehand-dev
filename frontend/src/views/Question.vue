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
    <hr>
    <div class="container">   
      <AnswerComponent
        v-for="(answer, index) in answers" 
        :answer="answer"
        :key="index"/>
    </div>
  </div>
</template>

<script>
import { apiService } from "../common/api.service.js";
import AnswerComponent from "@/components/Answer.vue";
export default {
  name: "Question",
  props: {
    id: {
      type: Number,
      required: true
    }
  },
  components: {
    AnswerComponent
  },
  data() {
    return {
      question: {},
      answers: []
    };
  },
  methods: {
    setPageTitle(title) {
      document.title = title;
    },
    getQuestionData() {
      let endpoint = `/api/questions/${this.id}/`;
      apiService(endpoint).then(data => {
        this.question = data;
        this.setPageTitle(data.etc);
      });
    },
    getQuestionAnswers() {
      let endpoint = `/api/questions/${this.id}/answers/`;
      apiService(endpoint).then(data => {
        this.answers = data.results;
        console.log(this.answers)
      });
    }
  },
  created() {
    this.getQuestionData();
    this.getQuestionAnswers()
    console.log(this.question);
  }
};
</script>
