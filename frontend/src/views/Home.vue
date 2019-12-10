<template>
  <div class="home">
    <div class="container">
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
    </div>
  </div>
</template>

<script>
import { apiService } from "../common/api.service";
export default {
  name: "home",
  data() {
    return {
      questions: []
    };
  },
  methods: {
    getQuestions() {
      let endpoint = "api/questions/";
      apiService(endpoint).then(data => {
        this.questions.push(...data.results);
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
