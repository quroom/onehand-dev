import Vue from "vue";
import moment from "moment";
import VueMomentJS from "vue-momentjs";
import VueRouter from "vue-router";
import AnswerEditor from "../views/AnswerEditor.vue";
import Home from "../views/Home.vue";
import Question from "../views/Question.vue";
import QuestionEditor from "../views/QuestionEditor.vue";

Vue.use(VueRouter);
Vue.use(VueMomentJS, moment);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
    props: true
  },
  {
    path: "/question/:id",
    name: "question",
    component: Question,
    props: true
    // props: (route) => {
    //   const id = Number.parseInt(route.params.id, 10)
    //   if (Number.isNaN(id)) {
    //     return 0
    //   }
    //   return { id }
    // }
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
