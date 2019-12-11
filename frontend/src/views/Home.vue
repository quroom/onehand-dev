<template>
  <div class="home">
    <div class="container mt-2">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">거래종류</th>
            <th scope="col">물건종류</th>
            <th scope="col">글제목(월세/매매가 등~?)</th>
            <th scope="col">글쓴이</th>
            <th scope="col">응답속도</th>
            <th scope="col">신뢰도</th>
            <th scope="col">등록일</th>
          </tr>
        </thead>
        <tbody v-for="question in questions" :key="question.id">
          <tr>
            <td>{{ question.item_category }}</td>
            <td>{{ question.trade_category }}</td>
            <td>
              <router-link
                :to="{ name: 'question', params: { id: question.id } }"
                class="question-link"
              >
                {{ question.etc }}
              </router-link>
              <span class="answer-count">({{ question.answers_count }})</span>
            </td>
            <td>
              {{ question.author }}
              <span class="answer-count">({{ question.answers_count }})</span>
            </td>
            <td>{{ question.average_response_time }}분</td>
            <td>reputation = 만족도 * 이행률</td>
            <td>{{ question.created_at }}</td>
          </tr>
          <hr />
        </tbody>
      </table>
      <div class="my-4">
        <p v-show="loadingQuestions">...로딩...</p>
        <button
          v-show="next"
          @click="getQuestions"
          class="btn btn-sm btn-outline-success"
          >
          Load More.
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from "../common/api.service";
export default {
  name: "home",
  data() {
    return {
      questions: [],
      next: null,
      loadingQuestions: false
    };
  },
  methods: {
    getQuestions() {
      let endpoint = "api/questions/";
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingQuestions = true
      apiService(endpoint).then(data => {
        this.questions.push(...data.results);
        this.loadingQuestions = false;
        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null
        }
      });
    }
  },
  created() {
    this.getQuestions();
    document.title = "원페이퍼";
    console.log(this.questions);
  }
};
</script>

<style scoped>
.answer-count {
  background-color: #f0f0f0;
}
.container {
  font-size: 12px;
}
.created-at {
  font-weight: bold;
  color: red;
}
.question-link {
  color: black;
}
</style>
