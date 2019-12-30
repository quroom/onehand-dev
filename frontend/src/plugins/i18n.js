import Vue from "vue";
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const messages = {
  en: {
    message: {
      etc: 'Additional information'
    }
  },
  ko: {
    message: {
      etc: '기타 요청사항'
    }
  }
}

// Create VueI18n instance with options
export const i18n = new VueI18n({
  locale: 'ko', // set locale
  messages, // set locale messages
})