<template>
  <ValidationObserver ref="obs">
    <div class="ma-5">
      <div class="headline mb-10 ml-5">집구하기 부터 이사까지 한번에!</div>
      <v-stepper v-model="e1">
        <v-stepper-header>
          <v-stepper-step key="0-step" :step="0" :complete="e1>0">{{$t('basic')}}</v-stepper-step>
          <template v-for="(key, index) in pros_category">
            <v-stepper-step
              :key="`${index+1}-step`"
              :step="index+1"
              :complete="e1>index+1"
            >{{PROS_CATEGORY[key]}}</v-stepper-step>
          </template>
        </v-stepper-header>
        <v-stepper-items>
          <v-stepper-content :key="`0-content`" :step="0">
            <ValidationObserver ref="0-step">
              <v-card class="mx-auto" outlined>
                <div class="subtitle">{{$t('basic')}} {{$t('info')}}</div>
                <v-row>
                  <v-col cols="12" sm="12" md="6">
                    <ValidationProvider rules="required" v-slot="{ errors, valid }">
                      <v-autocomplete
                        @change="prosChange"
                        v-model="pros_category"
                        :items="PROS_CATEGORY_LIST"
                        multiple
                        chips
                        deletable-chips
                        @input="searchInput=null"
                        :search-input.sync="searchInput"
                        label="필요업무(중개,법무사,가구구매 등)*"
                        :error-messages="errors"
                        :success="valid"
                      ></v-autocomplete>
                    </ValidationProvider>
                  </v-col>
                  <v-col cols="12" sm="6" md="3">
                    <ValidationProvider rules="required" v-slot="{ errors, valid }">
                      <v-autocomplete
                        v-model="item_category"
                        :items="ITEM_CATEGORY_LIST"
                        item-text="text"
                        item-value="value"
                        chips
                        label="물건종류(원룸,아파트,주택 등)*"
                        :error-messages="errors"
                        :success="valid"
                      ></v-autocomplete>
                    </ValidationProvider>
                  </v-col>
                </v-row>
                <v-row class="ma-0" justify="end">
                  <v-btn class="ma-1" @click="nextStep(0)">{{$t('next')}}</v-btn>
                </v-row>
              </v-card>
            </ValidationObserver>
          </v-stepper-content>
          <template v-for="(key, index) in pros_category">
            <v-stepper-content :key="`${index+1}-content`" :step="index+1">
              <ValidationObserver :ref="`${index+1}-step`">
                <v-card v-if="key=='REB'" class="mx-auto" outlined>
                  <div class="subtitle-1">{{$t('realestate')}} {{$t('info')}}</div>
                  <v-row>
                    <v-col
                      v-show="multiIncludes(pros_category, ['REB','TAX','RES','LAW'])"
                      cols="12"
                      sm="3"
                      md="3"
                    >
                      <ValidationProvider
                        :name="$t('transaction_category')"
                        rules="required"
                        v-slot="{ errors, valid }"
                      >
                        <v-autocomplete
                          v-model="transaction_category"
                          :items="TRANSACTION_CATEGORY_LIST"
                          item-text="text"
                          item-value="value"
                          chips
                          :label="$t('transaction_category')"
                          :error-messages="errors"
                          :success="valid"
                        ></v-autocomplete>
                      </ValidationProvider>
                    </v-col>
                    <v-col v-show="!multiIncludes(item_category, ['LND'])" cols="12" sm="3" md="2">
                      <ValidationProvider name="건물면적" rules="integer" v-slot="{ errors, valid }">
                        <v-text-field
                          v-model="building_area"
                          label="건물면적(㎡)"
                          :error-messages="errors"
                          :success="valid"
                        ></v-text-field>
                      </ValidationProvider>
                    </v-col>
                    <v-col
                      v-show=" multiIncludes(item_category, ['LND']) || (transaction_category=='TR' && multiIncludes(item_category, ['ONR','HOS','CMH','LND'])) "
                      cols="12"
                      sm="3"
                      md="2"
                    >
                      <v-text-field v-model="land_area" label="토지면적(㎡)"></v-text-field>
                    </v-col>
                    <v-col v-if="transaction_category=='TR'" cols="12" sm="3" md="2">
                      <v-text-field v-model="trade_price" label="매매가"></v-text-field>
                    </v-col>
                    <v-col
                      v-else-if="transaction_category=='DL' || transaction_category=='RT'"
                      cols="12"
                      sm="3"
                      md="2"
                    >
                      <v-text-field v-model="deposit" label="보증금" required></v-text-field>
                    </v-col>
                    <v-col v-if="transaction_category=='RT'" cols="12" sm="3" md="2">
                      <v-text-field v-model="monthly_fee" label="월세*" required></v-text-field>
                    </v-col>
                    <v-col col="12" sm="6" md="3">
                      <v-menu
                        v-model="cal_menu"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        transition="scale-transition"
                        offset-y
                        min-width="290px"
                      >
                        <template v-slot:activator="{on}">
                          <v-text-field
                            v-model="move_date"
                            label="희망 입주일"
                            prepend-icon="event"
                            readonly
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker
                          :day-format="date=>date.split('-')[2]"
                          locale="kr"
                          v-model="move_date"
                          @input="cal_menu=false"
                        ></v-date-picker>
                      </v-menu>
                    </v-col>
                  </v-row>
                  <v-row align="center">
                    <v-col cols="12" sm="12" md="8">
                      <AddressSearchComponent
                        label="주소 검색"
                        :button="true"
                        :address.sync="arv.address_objects"
                      ></AddressSearchComponent>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" xs="12">
                      <v-textarea
                        v-model="etc"
                        class="form-control"
                        :label="$t('etc')"
                        placeholder="요청 시 상세한 사항을 추가로 입력 해주세요. (입주 희망 아파트명, 세부지역, 세부조건 등)"
                        auto-grow
                        outlined
                      ></v-textarea>
                    </v-col>
                  </v-row>
                </v-card>
                <v-card v-else-if="key=='MOV'" class="mx-auto" outlined>
                  <div class="subtitle-1">이사 정보</div>
                  <v-row>
                    <v-col cols="12" sm="3" md="2">
                      <v-text-field
                        v-model="building_area"
                        label="출발지 건물 면적(㎡)"
                        hide-details="auto"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="3" md="2">
                      <v-text-field
                        v-model="building_area"
                        label="도착지 건물 면적(㎡)"
                        hide-details="auto"
                      ></v-text-field>
                    </v-col>
                    <v-col col="12" sm="6" md="3">
                      <v-menu
                        v-model="cal_menu2"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        transition="scale-transition"
                        offset-y
                        min-width="290px"
                      >
                        <template v-slot:activator="{on}">
                          <v-text-field
                            v-model="move_date"
                            label="이사 예정일"
                            prepend-icon="event"
                            readonly
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker
                          :day-format="date=>date.split('-')[2]"
                          locale="kr"
                          v-model="move_date"
                          @input="cal_menu2=false"
                        ></v-date-picker>
                      </v-menu>
                    </v-col>
                    <v-col cols="12" sm="6" md="3">
                      <v-autocomplete
                        v-model="move_category"
                        :items="MOVE_CATEGORY_LIST"
                        item-text="text"
                        item-value="value"
                        chips
                        label="이사종류(포장, 일반이사 등)*"
                        hide-details="auto"
                      ></v-autocomplete>
                    </v-col>
                    <v-col cols="12" sm="12" md="5">
                      <AddressSearchComponent label="출발지 검색" :address.sync="dep.address_objects"></AddressSearchComponent>
                    </v-col>
                    <v-col cols="12" sm="12" md="7">
                      <AddressSearchComponent
                        label="도착지 검색"
                        :button="true"
                        :address.sync="arv.address_objects"
                      ></AddressSearchComponent>
                    </v-col>
                  </v-row>
                </v-card>
                <v-row class="ma-1" justify="end">
                  <v-btn @click="prevStep(index+1)">{{$t('back')}}</v-btn>
                  <v-btn @click="nextStep(index+1)">{{$t('next')}}</v-btn>
                </v-row>
              </ValidationObserver>
            </v-stepper-content>
          </template>
        </v-stepper-items>
      </v-stepper>
      <v-container class="ma">
        <v-btn type="submit" color="primary" absolute @click="onSubmit()">제출</v-btn>
      </v-container>
    </div>
  </ValidationObserver>
</template>
<script>
import { apiService } from "../common/api.service.js";
import AddressSearchComponent from "@/components/AddressSearch.vue";
import { constants } from "@/components/mixins/constants.js";
import { ValidationObserver, ValidationProvider } from "vee-validate";
// import { CSRF_TOKEN } from '../common/csrf_token';
// import VueDaumPostcode from "vue-daum-postcode"

export default {
  mixins: [constants],
  name: "QuestionEditor",
  props: {
    id: {
      type: [Number, String],
      required: false
    }
  },
  components: {
    AddressSearchComponent,
    ValidationProvider,
    ValidationObserver
  },
  data() {
    return {
      arv: {
        address_objects: "",
        full_address: "",
        address: "",
        extra_address: ""
      },
      dep: {
        address_objects: "",
        full_address: "",
        address: "",
        extra_address: ""
      },
      e1: 0,
      address_dialog: false,
      address_key: 0,
      mandatory_input_rule: [[]],
      location_dialog: false,
      location_key: 0,
      floor_select: null,
      cal_menu: false,
      cal_menu2: false,
      land_area: 0,
      building_area: 0,
      trade_price: 0,
      deposit: 0,
      monthly_fee: 0,
      etc: null,
      end_date: null,
      move_category: null,
      move_date: null,
      item_category: null,
      transaction_category: null,
      pros_category: ["REB", "MOV"],
      searchInput: null,
      error: null,
      moment: null
    };
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
    stepper_changed(n) {
      console.log("stepper_n", n);
    },
    prevStep(n) {
      this.e1 = n - 1;
    },
    nextStep(n) {
      let observer_object = this.$refs[n + "-step"];
      if (Array.isArray(observer_object)) {
        if (observer_object.length == 1) {
          observer_object = observer_object[0];
        } else if (observer_object.length == 0) {
          console.log("There is not observer_object.");
        } else {
          console.log("Observer_object is more than one.");
        }
      }
      observer_object.validate();
      console.log(observer_object);

      if (!observer_object.flags.invalid) {
        if (n === this.pros_category.length) {
          this.e1 = 0;
        } else {
          this.e1 = n + 1;
        }
      }
    },
    prosChange() {
      this.pros_category.sort(
        (a, b) => this.PROS_CATEGORY_ORDER[a] - this.PROS_CATEGORY_ORDER[b]
      );
      console.log(this.pros_category);
    },
    handleAddress(data) {
      // this.fullAddress = data.address;
      // this.extraAddress = "";
      // if (data.addressType === "R") {
      //   if (data.bname !== "") {
      //     this.extraAddress += data.bname;
      //   }
      //   if (data.buildingName !== "") {
      //     this.extraAddress +=
      //       this.extraAddress !== ""
      //         ? `, ${data.buildingName}`
      //         : data.buildingName;
      //   }
      //   this.fullAddress +=
      //     this.extraAddress !== "" ? ` (${this.extraAddress})` : "";
      // }

      console.log(data); // e.g. '서울 성동구 왕십리로2길 20 (성수동1가)'
      // this.dialog=false
    },
    onSubmitAddress(flag) {
      //1:Departure address. 2:Arriving address. 3:Departure address partially.
      if (flag == 1) {
        this.dep.full_address = this.dep.address + " " + this.dep.extra_address;
        this.address_dialog = false;
        this.address_key += 1;
      } else if (flag == 2) {
        this.arv.full_address = this.arv.address + " " + this.arv.extra_address;
        this.address_dialog = false;
        this.address_key += 1;
      }
    },
    //Need to add code for exception control.
    onSubmit() {
      // console.log(self)
      let observer_object = this.$refs.obs;
      observer_object.validate().then(function(v) {
        console.log(v);
      });
      // console.log(observer_object.errors)
      if (!observer_object.flags.invalid) {
        if (!this.etc) {
          this.etc = "빔";
        }
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
          move_date: this.move_date,
          transaction_category: this.transaction_category,
          item_category: this.item_category,
          pros_category: this.pros_category,
          trade_price: this.trade_price,
          deposit: this.deposit,
          monthly_fee: this.monthly_fee
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
      return next(
        vm => (
          (vm.etc = data.etc),
          (vm.end_date = data.end_date),
          (vm.move_date = data.move_date),
          (vm.transaction_category = data.transaction_category),
          (vm.item_category = data.item_category),
          (vm.pros_category = data.pros_category),
          (vm.trade_price = data.trade_price),
          (vm.deposit = data.deposit),
          (vm.monthly_fee = data.monthly_fee)
        )
      );
    } else {
      return next();
    }
  },
  created() {
    document.title = "요청서 작성하기";
    this.end_date = this.$moment()
      .add(7, "days")
      .format("YYYY-MM-DD");
    this.move_date = this.$moment()
      .add(30, "days")
      .format("YYYY-MM-DD");
  }
};
</script>

<style scoped>
.theme--light.v-card.v-card--outlined {
  border: rgba(0, 0, 0, 0) !important;
}
</style>