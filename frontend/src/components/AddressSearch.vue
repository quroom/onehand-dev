<template>
  <v-row class="ml-0" align="center" @click.stop="button ? null : flag ? dialog = true : dialog2 = true">
    <v-text-field
      v-model="full_address"
      :label="label"
      outlined
      hide-details="auto"
      :readonly="full_address==''?true:false"
    ></v-text-field>
    <v-btn
      v-if="button"
      class="ml-5"
      @click.stop="dialog = true">
        상세주소로 검색
    </v-btn>
    <v-btn
      v-if="button"
      class="ml-5"
      @click.stop="dialog2 = true">
        지역으로 검색
    </v-btn>
    <v-dialog v-model="dialog">
      <v-card>
        <v-card-text class="pt-5">
          <vue-daum-postcode v-if="key%2==0" @complete="address_objects = $event; address = address_objects.jibunAddress + ' ' + address_objects.buildingName; extra_address=''; key+=1"/>
          <v-row v-else>
            <v-col class="pa-0" cols="12" sm="4">
              <v-text-field :value="this.address_objects.zonecode" label="우편번호" outlined readonly></v-text-field>
            </v-col>
            <v-col class="pa-0" cols="12" lg="12">
              <v-text-field v-model="address" outlined></v-text-field>
            </v-col>
            <v-text-field
              label="나머지 주소 입력"
              v-model="extra_address"
              outlined
            ></v-text-field>
            <v-btn @click.prevent="onSubmitAddress(1)">확인</v-btn>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog v-model="dialog2">
      <v-card>
        <v-card-text class="pt-5">
          <v-row align="center">
            <v-col cols="12" xs="6" md="2">
              <v-autocomplete label="시도"
                v-model="sido_select"
                :items="sido_list"
                item-text="brtcNm._text"
                item-value="brtcNm._text"
                @change="getLocationList('sigungu')"
              ></v-autocomplete>
            </v-col>
            <v-col cols="12" xs="6" md="2">
              <v-autocomplete label="시군구"
                v-model="sigungu_select"
                :items="sigungu_list"
                item-text="signguCd._text"
                item-value="signguCd._text"
                @change="getLocationList('eupmyundong')"
              ></v-autocomplete>
            </v-col>
            <v-col cols="12" xs="6" md="2">
              <v-autocomplete label="읍면동"
                v-model="eupmyundong_select"
                :items="eupmyundong_list"
                item-text="emdCd._text"
                item-value="emdCd._text"
              ></v-autocomplete>
            </v-col>
            <v-col cols="12" xs="6" md="2">
              <v-autocomplete label="층"
                v-model="floor_select"
                :items="FLOOR_LIST"
              ></v-autocomplete>
            </v-col>
            <v-col cols="12" md="1">
            <v-btn @click.prevent="onSubmitAddress(2)">확인</v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>        
  </v-row>
</template>
<script>
import { apiService2 } from "../common/api.service.js";
import { constants } from "@/components/mixins/constants.js";
var convert = require('xml-js');

export default {
  mixins: [constants],
  name: "AddressSearchComponent",
  props: {
    flag: {
      type: Boolean,
      required: false
    },
    label: {
      type: String,
      required: true
    },
    button: {
      type: Boolean,
      default: false,
    }
  },
  data() {
    return {
      dialog:false,
      dialog2:false,
      key:0,
      address:null,
      address_objects:null,
      full_address:'',
      extra_address:null,      
      floor_select: null,
      sido_select: null,
      sido_list: [],
      sigungu_select: null,
      sigungu_list: [],
      eupmyundong_select: null,
      eupmyundong_list: []
    }
  },
  methods: {
    onSubmitAddress(flag) {
      console.log("onSubmit")
      if(flag==1){
        this.full_address = this.address + " " + this.extra_address;
        this.$emit('update:address', this.address_objects)
        this.dialog=false
        this.key+=1
      } else if(flag==2) {
        this.full_address = this.sido_select + " " + this.sigungu_select + " " + this.eupmyundong_select + " " + this.floor_select
        this.dialog2 = false
        console.log(this.address)
      } else {
        console.log('3')
      }
    },
    getLocationList(flag) {
      console.log(flag)
      let endpoint = "/api/locationlist/"+flag+"/";
      if(flag=="sido") {
        this.location_dialog = true
        apiService2(endpoint).then(data => { 
            let json = convert.xml2json(data, {compact:true, ignoreComment:true})
            let json_obj = JSON.parse(json)
            if(json_obj.BorodCityResponse.cmmMsgHeader.returnCode._text == "00"){
              this.sido_list = json_obj.BorodCityResponse.borodCity
            }else{
              alert(JSON.parse(json_obj).EupMyunDongListResponse.cmmMsgHeader.errMsg)
            }
          });
      }else if(flag=="sigungu") {
        endpoint=endpoint+this.sido_select+"/";
        apiService2(endpoint).then(data => { 
            let json = convert.xml2json(data, {compact:true, ignoreComment:true})
            let json_obj = JSON.parse(json)
            if(json_obj.SiGunGuListResponse.cmmMsgHeader.returnCode._text == "00"){
              if(json_obj.SiGunGuListResponse.siGunGuList.length != undefined){
                this.sigungu_list = json_obj.SiGunGuListResponse.siGunGuList
              }else{
                this.sigungu_list = [{'signguCd':{'_text':this.sido_select}}]
              }
            }else {
              alert(JSON.parse(json_obj).EupMyunDongListResponse.cmmMsgHeader.errMsg)
            }
        });
      }else if(flag=="eupmyundong") {
        if(this.sido_select != this.sigungu_select){
          endpoint=endpoint+this.sido_select+"/"+this.sigungu_select+"/";
        }else {
          endpoint=endpoint+this.sido_select+"/";
        }        
        apiService2(endpoint).then(data => { 
            let json_obj = convert.xml2json(data, {compact:true, ignoreComment:true})
            this.eupmyundong_list = JSON.parse(json_obj).EupMyunDongListResponse.eupMyunDongList
        });
      }
    }
  },
  created() {    
    if(this.flag == false){      
      let endpoint = "/api/locationlist/sido/";
      apiService2(endpoint).then(data => { 
        let json = convert.xml2json(data, {compact:true, ignoreComment:true})
        let json_obj = JSON.parse(json)
        if(json_obj.BorodCityResponse.cmmMsgHeader.returnCode._text == "00"){
          this.sido_list = json_obj.BorodCityResponse.borodCity
        }else{
          alert(JSON.parse(json_obj).BorodCityResponse.cmmMsgHeader.errMsg)
        }
      });    
    }
  }  
}
</script>

<style>
.vue-daum-postcode-container {
  width: 100% !important;
  height: 444px !important;
}
</style>