import Vue from "vue";
import moment from "moment";
import VueMomentJS from "vue-momentjs";
import VueRouter from "vue-router";
import VueDaumPostcode from "vue-daum-postcode"
import AnswerEditor from "../views/AnswerEditor.vue";
import Home from "../views/Home.vue";
import Question from "../views/Question.vue";
import QuestionEditor from "../views/QuestionEditor.vue";

Vue.use(VueRouter);
Vue.use(VueMomentJS, moment);
Vue.use(VueDaumPostcode);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/question/:id",
    name: "question",
    component: Question,
    props: true
  },
  {
    path: "/ask/:id?",
    name: "question-editor",
    component: QuestionEditor,
    props: true
  },
  {
    path: "/answer/:id",
    name: "answer-editor",
    component: AnswerEditor,
    props: true
  }
];

const router = new VueRouter({
  mode: "history",
  // base: process.env.BASE_URL,
  routes
});

export default router;
