<template>
  <div class="ma-5">
    <v-container class="ma">
      <v-form @submit.prevent="onSubmit">
        <div class="headline mb-10">집구하기 부터 이사까지 한번에!</div>
        <div class="subtitle">기본정보</div>
        <v-row>
          <v-col cols="12" sm="12" md="6">
            <v-select
              @change="prosChange"
              v-model="pros_category"
              :items="PROS_CATEGORY_LIST"
              multiple
              chips
              deletable-chips
              label="필요업무(중개,법무사,가구구매 등)*"
            ></v-select>
          </v-col>
          <v-col
            v-show="multiIncludes(pros_category, ['REB','TAX','RES','LAW'])"
            cols="12"
            sm="6"
            md="3"
          >
            <v-select
              @change="transactionChange"
              v-model="transaction_category"
              :items="TRANSACTION_CATEGORY_LIST"
              item-text="text"
              item-value="value"
              chips
              label="거래종류(매매,전세,월세 등)*"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="item_category"
              :items="item_category_list"
              item-text="text"
              item-value="value"
              chips
              label="물건종류(원룸,아파트,주택 등)*"
            ></v-select>
          </v-col>
        </v-row>
        <div class="subtitle">부동산 조건 정보</div>
        <v-row>
          <v-col
            v-show="!multiIncludes(item_category, ['LND'])"
            cols="12"
            sm="3"
            md="2">
            <v-text-field v-model="building_area" label="건물면적(㎡)"></v-text-field>
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
        </v-row>
        <div class="subtitle">위치 및 일정 정보</div>
        <v-row outline>
          <v-col v-show="multiIncludes(pros_category, ['MOV'])" cols="12" sm="12" md="6">
            <v-text-field
              v-model="dep.full_address"
              label="출발 주소 검색"
              outlined
              readonly
              @click.stop="dep.dialog = true"
            ></v-text-field>
            <v-dialog v-model="dep.dialog" :key="dep.daumpostcodeKey">
              <v-card>
                <v-card-text class="pt-5">
                  <vue-daum-postcode v-if="dep.daumpostcodeKey%2==0" @complete="dep.address_objects = $event; dep.address = dep.address_objects.jibunAddress + ' ' + dep.address_objects.buildingName; dep.extra_address=''; dep.daumpostcodeKey+=1"/>
                  <v-row v-else>
                    <v-col class="pa-0" cols="12" sm="4">
                      <v-text-field :value="this.dep.address_objects.zonecode" label="우편번호" outlined readonly></v-text-field>
                    </v-col>
                    <v-col class="pa-0" cols="12" lg="12">
                      <v-text-field v-model="dep.address" outlined></v-text-field>
                    </v-col>
                    <v-text-field
                      label="나머지 주소 입력"
                      v-model="dep.extra_address"
                      outlined
                    ></v-text-field>
                    <v-btn @click.prevent="onSubmitAddress(1)">확인</v-btn>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-dialog>
          </v-col>
          <v-col
            v-show="multiIncludes(pros_category, ['REB','TAX','RES','LAW','INR','CLN', 'MOV', 'PRC'])"
            cols="12"
            sm="12"
            md="6"
          >
            <v-text-field
              v-if="multiIncludes(pros_category, ['MOV'])"
              v-model="arv.full_address"
              label="대상(도착) 주소 검색"
              outlined
              readonly
              @click.stop="arv.dialog = true"
            ></v-text-field>
            <v-text-field
              v-else-if="multiIncludes(pros_category, ['TAX','RES','LAW','INR','CLN', 'PRC'])"
              v-model="arv.full_address"
              label="대상 주소 검색"
              outlined
              readonly
              @click.stop="arv.dialog = true"
            ></v-text-field>
            <v-text-field
              v-else
              v-model="arv.address"
              label="입주 희망 지역 검색"
              outlined
              readonly
              @click.stop="arv.dialog = true"
            ></v-text-field>
            <v-dialog v-model="arv.dialog" :key="arv.daumpostcodeKey">
              <v-card>
                <v-card-text v-if="multiIncludes(pros_category, ['REB'])" class="pt-5">
                  <v-row>
                    <v-col cols="12" xs="12" md="3">
                      <v-select label="시도"></v-select>
                    </v-col>
                    <v-col cols="12" xs="12" md="3">
                      <v-select label="시군구"></v-select>
                    </v-col>
                    <v-col cols="12" xs="12" md="3">
                      <v-select label="읍면동"></v-select>
                    </v-col>
                    <v-col v-if="multiIncludes(pros_category, ['MOV'])" cols="12" xs="12" md="3">
                      <v-select label="층"></v-select>
                    </v-col>
                  </v-row>
                </v-card-text>
                <v-card-text v-else class="pt-5">
                  <vue-daum-postcode v-if="arv.daumpostcodeKey%2==0" @complete="arv.address_objects = $event; arv.address = arv.address_objects.jibunAddress + ' ' + arv.address_objects.buildingName; arv.extra_address=''; arv.daumpostcodeKey+=1"/>
                  <v-row v-else>
                    <v-col class="pa-0" cols="12" sm="4">
                      <v-text-field :value="this.arv.address_objects.zonecode" label="우편번호" outlined readonly></v-text-field>
                    </v-col>
                    <v-col class="pa-0" cols="12" lg="12">
                      <v-text-field v-model="arv.address" outlined></v-text-field>
                    </v-col>
                    <v-text-field
                      label="나머지 주소 입력"
                      v-model="arv.extra_address"
                      outlined
                    ></v-text-field>
                    <v-btn @click.prevent="onSubmitAddress(2)">확인</v-btn>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-dialog>
          </v-col>
          <v-col v-show="multiIncludes(pros_category, ['MOV'])" col="12" sm="6" md="3">
            <v-menu
              v-model="menu"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template v-slot:activator="{on}">
                <v-text-field
                  v-model="moving_date"
                  label="이사 예정일"
                  prepend-icon="event"
                  readonly
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                :day-format="date=>date.split('-')[2]"
                locale="kr"
                v-model="moving_date"
                @input="menu=false"
              ></v-date-picker>
            </v-menu>
          </v-col>
        </v-row>
        <v-textarea
          v-model="etc"
          class="form-control mt-5"
          :label="$t('message.etc')"
          placeholder="요청시 상세한 사항을 추가로 입력 해주세요. (입주 희망 아파트명, 세부지역, 세부조건 등)"
          auto-grow
          outlined
        ></v-textarea>
        <v-btn type="submit" color="primary" absolute>제출</v-btn>
      </v-form>
    </v-container>
  </div>
</template>
<script>
import { apiService } from "../common/api.service.js";
import { constants } from "@/components/mixins/constants.js";
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
  data() {
    return {
      arv:{
        daumpostcodeKey:0,
        address_objects: "",
        full_address:"",
        address:"",
        extra_address: "",
        dialog: false,
      },
      dep:{
        daumpostcodeKey:0,
        address_objects: "",
        full_address:"",
        address:"",
        extra_address: "",
        dialog: false,
      },
      menu: false,
      item_category_list: [],
      land_area: 0,
      building_area: 0,
      trade_price: 0,
      deposit: 0,
      monthly_fee: 0,
      etc: null,
      end_date: null,
      moving_date: null,
      item_category: null,
      transaction_category: null,
      pros_category: ["REB", "MOV"],
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
    prosChange() {
      console.log(this);
    },
    transactionChange() {
      console.log(this.item_category_list);
      if (this.transaction_category == "TR") {
        console.log("tr");
        console.log(this.item_category_list.splice(1, 3));
      } else {
        this.item_category_list = JSON.parse(
          JSON.stringify(this.ITEM_CATEGORY_LIST)
        );
      }
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
      if(flag==1){
        this.dep.full_address = this.dep.address + " " + this.dep.extra_address
        this.dep.dialog = false
        this.dep.daumpostcodeKey+=1      
      } else if(flag==2) {
        this.arv.full_address = this.arv.address + " " + this.arv.extra_address
        this.arv.dialog = false
        this.arv.daumpostcodeKey+=1
      } else {
        console.log('3')
      }
    },
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
          (vm.moving_date = data.moving_date),
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
    this.item_category_list = JSON.parse(
      JSON.stringify(this.ITEM_CATEGORY_LIST)
    );
    // this.end_date = '1900-01-01'
    // this.moving_date ='1900-01-01'
    this.end_date = this.$moment()
      .add(7, "days")
      .format("YYYY-MM-DD");
  }
};
</script>