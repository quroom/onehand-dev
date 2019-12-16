<template>
  <div class="single-question mt-2">
    <div class="container">
      <QuestionActions
        v-if="isQuestionAuthor"
        :id="id"
      />
      <h1>
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
        :requestUser="requestUser"
        :key="index"
        @delete-answer="deleteAnswer"/>
        <div class="my-4">
        <p v-show="loadingAnswers">...로딩...</p>
        <button
          v-show="next"
          @click="getQuestionAnswers"
          class="btn btn-sm btn-outline-success"
          >
          Load More.
        </button>
      </div>
      <hr>
      <div v-if="userHasAnswered">
        <p class="answer-added">You've written an answer!</p>
      </div>
      <div v-else-if="showForm">
        <form class="card" @submit.prevent="onSubmit">
          <div class="card-header px-3">
            Answer the Question
          </div>
          <div class="card-block">
            <textarea v-model="newAnswerBody" class="form-control" placeholder="당신의 능력으로 도움을 주세요." rows="5"></textarea>
          </div>
          <div class="card-footer px-3">
            <button type="submit" class="btn btn-sm btn-success">Submit Your Answer</button>
          </div>
        </form>
      </div>
      <div v-else>
        <button class="btn btn-sm btn-success" @click="showForm=true">
          Answer the Question
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from "../common/api.service.js";
import AnswerComponent from "@/components/Answer.vue";
import QuestionActions from "@/components/QuestionActions.vue";
export default {
  name: "Question",
  props: {
    id: {
      type: [Number,String],
      required: true
    }
  },
  components: {
    AnswerComponent,
    QuestionActions
  },
  data() {
    return {
      question: {},
      answers: [],
      newAnswerBody: null,
      error: null,
      userHasAnswered: false,
      showForm: false,
      next: null,
      loadingAnswers: false,
      requestUser: null
    };
  },
  computed: {
    isQuestionAuthor() {
      return this.question.author === this.requestUser;
    }
  },
  methods: {
    setPageTitle(title) {
      document.title = title;
    },
    setRequestUser() {
      this.requestUser = window.localStorage.getItem("username");
    },
    getQuestionData() {
      let endpoint = `/api/questions/${this.id}/`;
      apiService(endpoint).then(data => {
        this.question = data;
        this.userHasAnswered = data.user_has_answered;
        this.setPageTitle(data.etc);
      });
    },
    getQuestionAnswers() {
      let endpoint = `/api/questions/${this.id}/answers/`;
      this.loadingAnswers = true
      if (this.next) {
        endpoint = this.next
      }
      apiService(endpoint).then(data => {
        this.answers.push(...data.results);
        this.loadingAnswers = false;
        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null
        }
        console.log(this.answers)
      });
    },
    onSubmit() {
      if (this.newAnswerBody) {
        let endpoint = `/api/questions/${this.id}/answer/`;
        apiService(endpoint, "POST", {body: this.newAnswerBody}).then(data => {
          this.answers.unshift(data)
        })
        this.newAnswerBody = null;
        this.showForm = false;
        this.userHasAnswered = true;
        if (this.error) {
          this.error = null;
        }
      } else {
        this.error = "답변을 채워주세요."
      }
    },
    async deleteAnswer(answer) {
      let endpoint = `/api/answers/${answer.id}/`;
      try {
        await apiService(endpoint, "DELETE")
        this.$delete(this.answers, this.answers.indexOf(answer))
        this.userHasAnswe
      } catch (err) {
        console.log(err)
      }
    }
  },
  created() {
    this.getQuestionData();
    this.getQuestionAnswers();
    this.setRequestUser()
    console.log(this.question);
  }
};
</script>

<style scoped>
.author-name {
  font-weight: bold;
  color: #DC3545;
}

.answer-added {
  font-weight: bold
}

.error {
  font-weight: bold;
  color: red;
}
</style>