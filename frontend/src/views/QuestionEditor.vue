<template>
  <v-container class="my-5">
    <v-form @submit.prevent="onSubmit">
      <h1 class="mb-3">일괄 요청서 작성</h1>
      <v-menu
        v-model="menu2"
        :close-on-content-click="false"
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        min-width="290px"
      >
        <template v-slot:activator="{ on }">
          <v-text-field
            min-width="290px"
            v-model="end_date"
            label="질문 마감일"
            prepend-icon="event"
            readonly
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker
          :day-format="date => date.split('-')[2]"
          locale="ko"
          v-model="end_date"
          @input="menu2 = false"
        ></v-date-picker>
      </v-menu>
      <v-menu
        v-model="menu"
        :close-on-content-click="false"
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        min-width="290px"
      >
        <template v-slot:activator="{ on }">
          <v-text-field
            v-model="moving_date"
            label="이사 예정일"
            prepend-icon="event"
            readonly
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker
          :day-format="date => date.split('-')[2]"
          locale="kr"
          v-model="moving_date"
          @input="menu = false"
        ></v-date-picker>
      </v-menu>
      <v-select
        v-model="pros_category"
        :items="PROS_CATEGORY_LIST"
        multiple
        label="필요업무(중개,법무사,가구구매 등)"
      ></v-select>
      <v-select
        v-model="item_category"
        :items="ITEM_CATEGORY_LIST"
        item-text="text"
        item-value="value"
        label="물건종류(원룸,아파트,주택 등)"
      ></v-select>
      <v-select
        v-model="trade_category"
        :items="TRADE_CATEGORY_LIST"
        item-text="text"
        item-value="value"
        label="거래종류(매매,전세,월세 등)"
      ></v-select>
      <v-text-field v-if="trade_category==1" v-model="trade_price" label="매매가"></v-text-field>
      <v-text-field
        v-else-if="trade_category==2 || trade_category==3"
        v-model="trade_price"
        label="보증금"
        required
      ></v-text-field>
      <v-text-field v-if="trade_category==3" v-model="trade_price" label="월세*" required></v-text-field>
      <v-textarea
        v-model="etc"
        class="form-control"
        label="기타 요청사항"
        placeholder="요청시 필요한 사항을 추가로 입력 해주세요."
        rows="3"
      ></v-textarea>
      <v-btn type="submit" color="primary" absolute>제출</v-btn>
    </v-form>
  </v-container>
</template>
<script>
import { apiService } from "../common/api.service.js";
import { constants } from "@/components/mixins/constants.js";

export default {
  mixins: [constants],
  name: "QuestionEditor",
  props: {
    id: {
      type: [Number, String],
      required: false
    }
  },
  data() {
    return {
      trade_price: null,
      deposit: null,
      monthly_fee: null,
      etc: null,
      end_date: null,
      moving_date: null,
      item_category: null,
      trade_category: null,
      pros_category: [],
      menu: false,
      menu2: false,
      error: null,
      moment: null
    };
  },
  methods: {
    onSubmit() {
      if (!this.etc) {
        this.etc = "빔";
      } else {
        let endpoint = "/api/questions/";
        let method = "POST";
        if (this.id !== undefined) {
          endpoint += `${this.id}/`;
          method = "PUT";
        }
        console.log(this);
        apiService(endpoint, method, {
          etc: this.etc,
          end_date: this.end_date,
          moving_date: this.moving_date,
          trade_category: this.trade_category,
          item_category: this.item_category,
          pros_category: this.pros_category
        }).then(data => {
          this.$router.push({
            name: "question",
            params: { id: data.id }
          });
        });
      }
    }
  },
  async beforeRouteEnter(to, from, next) {
    if (to.params.id !== undefined) {
      let endpoint = `/api/questions/${to.params.id}/`;
      let data = await apiService(endpoint);
      return next(vm => (
        vm.etc = data.etc,
        vm.end_date = data.end_date,
        vm.moving_date = data.moving_date,
        vm.trade_category = data.trade_category,
        vm.item_category = data.item_category,
        vm.pros_category = data.pros_category
        ));
    } else {
      return next();
    }
  },
  created() {
    document.title = "요청서 작성하기";
    this.end_date = this.$moment()
      .add(7, "days")
      .format("YYYY-MM-DD");
  }
};
</script>
