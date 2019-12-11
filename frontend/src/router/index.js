import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Question from "../views/Question.vue";
import QuestionEditor from "../views/QuestionEditor.vue";

Vue.use(VueRouter);

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
    props: (route) => {
      const id = Number.parseInt(route.params.id, 10)
      if (Number.isNaN(id)) {
        return 0
      }
      return { id }
    }
  },
  {
    path: "/ask",
    name: "question-editor",
    component: QuestionEditor
  }
];

const router = new VueRouter({
  mode: "history",
  // base: process.env.BASE_URL,
  routes
});

export default router;
