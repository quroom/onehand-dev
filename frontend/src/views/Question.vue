<template>
  <div class="ma-5">
    <v-container class="my-5">
      <div class="headline mb-10 ml-5">집구하기 부터 이사까지 한번에!</div>
      <v-row>
        <v-col class="pb-0" cols="12" xs="12" md="4">
          <v-icon left color="blue">mdi-account</v-icon>
          <span>{{question.author}}</span>
        </v-col>
        <v-col class="pb-0" cols="12" xs="12" md="4">
          <v-row align="center" style="height:100%">
            <span>등록일: {{ question.created_at }}</span>
          </v-row>
        </v-col>
        <v-col class="pt-0" cols="12" xs="12" md="12">
          <v-row>
            <v-subheader>
              필요업무
            </v-subheader>
            <div class="mt-2">
              <v-chip class="mr-2" color="green" text-color="white" v-for="pro in question.pros_category" :key="pro">
                {{ PROS_CATEGORY[pro] }}
              </v-chip>
            </div>
            <v-subheader class="ml-4">
              물건정보
            </v-subheader>
            <v-chip class="mt-2" color="primary">{{ ITEM_CATEGORY[question.item_category] }}</v-chip>
            <v-chip class="mt-2 ml-2" color="primary">{{ TRANSACTION_CATEGORY[question.transaction_category] }}</v-chip>
          </v-row>
        </v-col>
      </v-row>
      <v-divider></v-divider>
      <v-stepper v-model="e1">
        <v-stepper-header>
          <v-stepper-step key="0-step" :step="0" :complete="e1>0">{{$t('all')}}{{$t('info')}}</v-stepper-step>
          <template v-for="(key, index) in question.pros_category">
            <v-stepper-step
              :key="`${index+1}-step`"
              :step="index+1"
              :complete="e1>index+1"
            >{{PROS_CATEGORY[key]}}</v-stepper-step>
          </template>
        </v-stepper-header>
      </v-stepper>
      <div class="subtitle mt-5">부동산 조건 정보</div>
      <v-row>
        <v-col
            v-show="!multiIncludes(question.item_category, ['LND'])"
            cols="12"
            sm="3"
            md="2">
            <v-text-field v-model="question.building_area" label="건물면적(㎡)" readonly></v-text-field>
          </v-col>
          <v-col
            v-show=" multiIncludes(question.item_category, ['LND']) || (question.transaction_category=='TR' && multiIncludes(question.item_category, ['ONR','HOS','CMH','LND'])) "
            cols="12"
            sm="3"
            md="2"
          >
            <v-text-field v-model="question.land_area" label="토지면적(㎡)" readonly></v-text-field>
          </v-col>
          <v-col v-if="question.transaction_category=='TR'" cols="12" sm="3" md="2">
            <v-text-field v-model="question.trade_price" label="매매가" readonly></v-text-field>
          </v-col>
          <v-col
            v-else-if="question.transaction_category=='DL' || question.transaction_category=='RT'"
            cols="12"
            sm="3"
            md="2"
          >
            <v-text-field v-model="question.deposit" label="보증금" readonly></v-text-field>
          </v-col>
          <v-col v-if="question.transaction_category=='RT'" cols="12" sm="3" md="2" readonly>
            <v-text-field v-model="question.monthly_fee" label="월세*" readonly></v-text-field>
          </v-col>
      </v-row>
      <div class="subtitle">위치 및 일정 정보</div>
      <v-row outline>
      </v-row>
      <v-row class="mb-0">
        <v-col class="pb-0" cols="12">
          <v-textarea label="기타요청사항" v-model="question.etc" auto-grow outlined readonly></v-textarea>
        </v-col>
      </v-row>
      <v-row>
        <v-col class="pt-0" cols="12">
          <v-row justify="end">
            <QuestionActions v-if="isQuestionAuthor" :id="id" />
          </v-row>
        </v-col>
      </v-row>
      <hr />
      <div class="container">
        <AnswerComponent
          v-for="(answer, index) in answers"
          :answer="answer"
          :requestUser="requestUser"
          :key="index"
          @delete-answer="deleteAnswer"
        />
        <div class="my-4">
          <p v-show="loadingAnswers">...로딩...</p>
          <button
            v-show="next"
            @click="getQuestionAnswers"
            class="btn btn-sm btn-outline-success"
          >Load More.</button>
        </div>
        <hr />
        <div v-if="userHasAnswered">
          <p class="answer-added">You've written an answer!</p>
        </div>
        <div v-else-if="showForm">
          <form class="card" @submit.prevent="onSubmit">
            <div class="card-header px-3">Answer the Question</div>
            <div class="card-block">
              <textarea
                v-model="newAnswerBody"
                class="form-control"
                placeholder="당신의 능력으로 도움을 주세요."
                rows="5"
              ></textarea>
            </div>
            <div class="card-footer px-3">
              <button type="submit" class="btn btn-sm btn-success">Submit Your Answer</button>
            </div>
          </form>
        </div>
        <div v-else>
          <button class="btn btn-sm btn-success" @click="showForm = true">Answer the Question</button>
        </div>
      </div>
    </v-container>
  </div>
</template>

<script>
import { apiService } from "../common/api.service.js";
import AnswerComponent from "@/components/Answer.vue";
import QuestionActions from "@/components/QuestionActions.vue";
import { constants } from "@/components/mixins/constants.js";
import { getCookie } from "../common/get_cookie.js"
export default {
  mixins: [constants],
  name: "Question",
  props: {
    id: {
      type: [Number, String],
      required: true
    }
  },
  components: {
    AnswerComponent,
    QuestionActions
  },
  data() {
    return {
      e1: 0,
      question: {},
      answers: [],
      newAnswerBody: null,
      error: null,
      userHasAnswered: false,
      showForm: false,
      next: null,
      loadingAnswers: false,
      requestUser: null,
    };
  },
  computed: {
    isQuestionAuthor() {
      return this.question.author === this.requestUser;
    }
  },
  methods: {
    multiIncludes(selected_category, condition_category) {
      if (Array.isArray(selected_category)) {
        for (let value of selected_category) {
          if (condition_category.includes(value)) {
            return true;
          }
        }
      } else {
        for (let value of condition_category) {
          if (selected_category == value) {
            return true;
          }
        }
      }
      return false;
    },
    getCookie:getCookie,
    setPageTitle(title) {
      document.title = title;
    },
    setRequestUser() {
      this.requestUser = window.localStorage.getItem("username");
    },
    getQuestionData() {
      let endpoint = `/api/questions/${this.id}/`;
      apiService(endpoint).then(data => {
        //Sort for pros_category
        data.pros_category.sort((a, b) => this.PROS_CATEGORY_ORDER[a] - this.PROS_CATEGORY_ORDER[b]);
        this.question = data;
        this.userHasAnswered = data.user_has_answered;
        this.setPageTitle(data.etc);
      });
    },
    getQuestionAnswers() {
      let endpoint = `/api/questions/${this.id}/answers/`;
      this.loadingAnswers = true;
      if (this.next) {
        endpoint = this.next;
      }
      apiService(endpoint).then(data => {
        this.answers.push(...data.results);
        this.loadingAnswers = false;
        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null;
        }
        console.log(this.answers);
      });
    },
    onSubmit() {
      if (this.newAnswerBody) {
        let endpoint = `/api/questions/${this.id}/answer/`;
        apiService(endpoint, "POST", { body: this.newAnswerBody }).then(
          data => {
            this.answers.unshift(data);
          }
        );
        this.newAnswerBody = null;
        this.showForm = false;
        this.userHasAnswered = true;
        if (this.error) {
          this.error = null;
        }
      } else {
        this.error = "답변을 채워주세요.";
      }
    },
    async deleteAnswer(answer) {
      let endpoint = `/api/answers/${answer.id}/`;
      try {
        await apiService(endpoint, "DELETE");
        this.$delete(this.answers, this.answers.indexOf(answer));
        this.userHasAnswered = false;
      } catch (err) {
        console.log(err);
      }
    }
  },
  created() {
    if(!getCookie('islogin')){
      window.location.href='/accounts/login/'
    }else{
      this.getQuestionData();
      this.getQuestionAnswers();
      this.setRequestUser();
      console.log(this.question);
    }
  }
};
</script>

<style scoped>
.author-name {
  font-weight: bold;
  color: #dc3545;
}

.answer-added {
  font-weight: bold;
}

.error {
  font-weight: bold;
  color: red;
}
</style>
