<template>
  <div class="question-actions">
    <router-link
      :to="{name: 'question-editor', params: {id: id}}"
      class="btn btn-sm btn-outline-secondary mr-1"
      >Edit
    </router-link>
    <button
      class="btn btn-sm btn-outline-danger"
      @click="deleteQuestion"
    >Delete</button>
  </div>
</template>

<script>
import { apiService } from "../common/api.service.js";
export default {
  name: "QuestionActions",
  props: {
    id: {
      type: [Number,String],
      required: true
    }
  },
  methods: {
    async deleteQuestion() {
      let endpoint = `/api/questions/${this.id}/`;
      try {
        await apiService(endpoint, "DELETE")
        this.$router.push("/");
      }
      catch (err) {
        console.log(err);
      }
    }
  }
}
</script>