var v = new Vue({
  el: '#app',
  delimiters: ['${','}'],
  data: {
    lists: [],
    list_id: 0,
    parent_id: 0,
    question: '',
    answers: [],
//    answer_id: 0,
    loading: true
  },
  created() {
    let api_url = 'http://localhost:8000/api/dialogs/?format=json&parent=null';
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
      let api_url = 'http://localhost:8000/api/dialogs/?format=json&parent=' + this.list_id;
      this.loading = true;
      this.$http.get(api_url)
          .then((response) => {
            this.loading = false;
            data = response.data;
            this.question = this.answer_text;
            for (var key in data) {
                this.answers[key] = {"parent_id": data[key].id, "answer_text": data[key].answer_text, "choice_text": data[key].choice_text};
                }
          })
          .catch((err) => {
            this.loading = false;
            console.log(err);
          })
    },

    get_first_question(list_id, answer_text) {
        this.list_id = list_id;
        this.answer_text = answer_text;
        this.get_question();
    },

    get_next_question(list_id, answer_text) {
        this.list_id = list_id;
        this.answer_text = answer_text;
        this.answers = [];
        this.get_question();
    },

    has_answer() {
        return !!this.answers;
    },

    can_answer() {
        return this.answers.length > 0;
    }

  }
});