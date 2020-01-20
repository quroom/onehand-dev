<template>
  <div class="home">
    <v-container class="my-5">
      <v-layout row wrap>
        <v-flex xs12 sm6 md4 lg3 v-for="question in questions" :key="question.id">
          <v-card
            class="text-xs-center ma-3"
            flat
            outlined
            :to="{ name: 'question', params: { id: question.id } }"
          >
            <v-card-title
              class="headline ma-1"
            >{{ITEM_CATEGORY[question.item_category]+' '+ TRANSACTION_CATEGORY[question.transaction_category]}} ({{ question.answers_count }})</v-card-title>
            <v-card-subtitle class="pb-1">
              <span>{{question.to_location}}</span>
              <span class="item_price" v-if="question.transaction_category=='TR'">매{{question.trade_price}}원</span>
              <span class="item_price" v-else-if="question.transaction_category=='DL'">보{{question.deposit}}원</span>
              <span
                class="item_price"
                v-else-if="question.transaction_category=='RT'"
              >보{{question.deposit}}원/월{{question.monthly_fee}}원</span>
            </v-card-subtitle>
            <v-card-text class="multiline-ellipsis pt-1 pb-0">{{question.etc}}</v-card-text>
            <v-card-text>
              <v-chip-group
                multiple
                column
                dark
                active-class="primary--text"
              >
                <v-chip color="green" v-for="pro in question.pros_category" :key="pro">
                  {{ PROS_CATEGORY[pro] }}
                </v-chip>
              </v-chip-group>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>

      <router-link v-show="getCookie('islogin')" :to="{ name: 'question-editor' }">
        <v-btn absolute dark fab mid right color="grey">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </router-link>
      <!-- <table class="table">
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
      </table>-->
      <div class="my-4">
        <p v-show="loadingQuestions">...로딩...</p>
        <button
          v-show="next"
          @click="getQuestions"
          class="btn btn-sm btn-outline-success"
        >Load More.</button>
      </div>
    </v-container>
  </div>
</template>

<script>
import { apiService } from "../common/api.service";
import { constants } from "@/components/mixins/constants.js";
import { getCookie } from "@/common/get_cookie.js";

export default {
  mixins: [constants],
  name: "home",
  data() {
    return {
      headers: [
        { text: "거래종류", value: "trade_category" },
        { text: "물건종류", value: "item_category" },
        { text: "제목:월세가 등 입력", value: "etc" },
        { text: "글쓴이", value: "author" },
        { text: "응답속도", value: "average_response_time" },
        { text: "신뢰도", value: "" },
        { text: "등록일", value: "created_at" }
      ],
      questions: [],
      next: null,
      loadingQuestions: false,
    };
  },
  methods: {
    getCookie:getCookie,
    getQuestions() {
      let endpoint = "api/questions/";
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingQuestions = true;
      apiService(endpoint).then(data => {
        this.questions.push(...data.results);
        this.loadingQuestions = false;
        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null;
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
.item_price {
  float: right;
}
.multiline-ellipsis {
  overflow: hidden;
  position: relative;
  line-height: 20px;
  max-height: 105px;
  text-align: justify;
  margin-right: -1em;
  padding-right: 1em;
}
.multiline-ellipsis:before {
  content: "...";
  position: absolute;
  right: 0;
  bottom: 0;
}
.multiline-ellipsis:after {
  content: "";
  position: absolute;
  right: 0;
  width: 1em;
  height: 1em;
  margin-top: 0.2em;
  background: white;
}
</style>
