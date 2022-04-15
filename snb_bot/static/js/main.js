var v = new Vue({
  el: '#app',
  delimiters: ['${','}'],
  data: {
    lists: [],
    list_id: 0,
    question: '',
    answers: [],
    answer_id: 0,
    loading: true
  },
  created() {
    let api_url = 'api/lists/?format=json';
      this.loading = true;
      this.$http.get(api_url)
          .then((response) => {
            this.loading = false;
            this.lists = response.data;
          })
          .catch((err) => {
            this.loading = false;
            console.log(err);
          })
  },
  methods: {
    get_question() {
      let api_url = 'api/questions/?format=json&list=' + this.list_id;
      if (this.answer_id) {
        api_url += '&answer=' + this.answer_id;
      }
      this.loading = true;
      this.$http.get(api_url)
          .then((response) => {
            this.loading = false;
            data = response.data;
            this.question = data.text;
            this.answers = data.answers;
            this.answer_id = '';
          })
          .catch((err) => {
            this.loading = false;
            console.log(err);
          })
    },

    get_first_question(list_id) {
        this.list_id = list_id;
        this.answer_id = '';
        this.get_question();
    },

    get_next_question() {
        this.get_question();
    },

    has_answer() {
        return !!this.answer_id;
    },

    can_answer() {
        return this.answers.length > 0;
    }

  }
});
