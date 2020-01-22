import {i18n} from '@/plugins/i18n';

export const constants = {
  data() {
    return {
      ITEM_CATEGORY: {
        'ONR': "원룸",
        'TWR': "투룸",
        'THR': "쓰리룸",
        'FOR': "포룸",
        'SHH': "쉐어하우스",
        'OFT': "오피스텔",
        'APT': "아파트",
        'VIL': "빌라",
        'HOS': "단독주택",
        'CMH': "상가주택",
        'STO': "상가",
        'LND': "토지"
      },
      TRANSACTION_CATEGORY: {
        'TR': "매매",
        'DL': "전세",
        'RT': "월세",
        // 'EX': "교환",
        'CS': "상담"
      },
      PROS_CATEGORY: {
        'REB': i18n.t("brokerage"),
        // 'TAX': "세무",
        // 'RES': "등기",
        // 'LAW': "법률",
        // 'LON': "대출",
        // 'INR': "인테리어",
        // 'CLN': "청소",
        'MOV': i18n.t("move"),
        // 'PRC': "입주사전점검",
        // 'HAP': "가전구매",
        // 'FRP': "가구구매"
      },
      PROS_CATEGORY_ORDER: {
        'REB': 1,
        'TAX': 2,
        'RES': 3,
        'LAW': 4,
        'LON': 5,
        'INR': 6,
        'CLN': 7,
        'MOV': 8,
        'PRC': 10,
        'HAP': 11,
        'FRP': 12
      },
      MOVE_CATEGORY_LIST: [
        { value: 'PMV', text: '포장이사'},
        { value: 'HMV', text: '반포장이사'},
        { value: 'NMV', text: '일반이사'},
      ],
      ITEM_CATEGORY_LIST: [
        { value: 'ONR', text: "원룸" },
        { value: 'TWR', text: "투룸" },
        { value: 'THR', text: "쓰리룸" },
        { value: 'FOR', text: "포룸" },
        { value: 'SHH', text: "쉐어하우스" },
        { value: 'OFT', text: "오피스텔" },
        { value: 'APT', text: "아파트" },
        { value: 'VIL', text: "빌라" },
        { value: 'HOS', text: "단독주택" },
        { value: 'CMH', text: "상가주택" },
        { value: 'STO', text: "상가" },
        { value: 'LND', text: "토지" }
      ],
      TRANSACTION_CATEGORY_LIST: [
        { value: 'TR', text: "매매" },
        { value: 'RT', text: "월세" },
        { value: 'DL', text: "전세" },
        // { value: 'EX', text: "교환" },
        { value: 'CS', text: "상담" }
      ],
      PROS_CATEGORY_LIST: [
        { value: 'REB', text: i18n.t("brokerage") },
        // { value: 'TAX', text: "세무" },
        // { value: 'RES', text: "등기" },
        // { value: 'LAW', text: "법률" },
        // { value: 'LON', text: "대출" },
        // { value: 'INR', text: "인테리어" },
        // { value: 'CLN', text: "청소" },
        { value: 'MOV', text: i18n.t("move") },
        // { value: 'PRC', text: "입주사전점검" },
        // { value: 'HAP', text: "가전구매" },
        // { value: 'FRP', text: "가구구매" }
      ],
      FLOOR_LIST: [
        { value: 0, text: "상관없음" },
        { value: 1, text: "1층" },
        { value: 2, text: "저층" },
        { value: 3, text: "로얄층" },
        { value: 4, text: "고층" },
        { value: 5, text: "탑층" }
      ]
    };
  }
};
