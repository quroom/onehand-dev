<template>
  <div>
    <v-btn text color="grey" :to="{ name: 'question-editor', params: { id: id } }">
      <span>수정</span>
      <v-icon>edit</v-icon>
    </v-btn>
    <v-btn text color="grey" @click="deleteQuestion">
      <span>삭제</span>
      <v-icon>delete</v-icon>
    </v-btn>
  </div>
</template>

<script>
import { apiService } from "../common/api.service.js";
export default {
  name: "QuestionActions",
  props: {
    id: {
      type: [Number, String],
      required: true
    }
  },
  methods: {
    async deleteQuestion() {
      let endpoint = `/api/questions/${this.id}/`;
      try {
        await apiService(endpoint, "DELETE");
        this.$router.push("/");
      } catch (err) {
        console.log(err);
      }
    }
  }
};
</script>
