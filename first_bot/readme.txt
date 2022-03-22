Результат - работающее Django-приложение. У него будет главная страница и админ-страница. Также я бы хотел, чтобы ты подключил Swagger. Еще это все должно быть докеризировано. Статичные файлы должны обрабатываться nginx-ом, динамика идти на Django, это корпоративный стандарт.

Данные должны храниться в базе Postgres, первоначальное наполнение (seed) должно идти из текстового файле в JSON или YAML-формате.

http://0.0.0.0 - main page

http://0.0.0.0/admin/ admin

http://0.0.0.0/api/ available API

http://0.0.0.0/api/lists/ questionnaires list

http://0.0.0.0/api/questions/?list=[LIST_ID] initial question of the given questionnaires list

http://0.0.0.0/api/questions/?list=[LIST_ID]&answer=[QUESTION_ID] - question on answer of the given questionnaires list

Вот база знаний, можешь что-то свое туда добавить, это просто пример:
[
  [
    "Menu",
    "Are you hungry?",
    [
      [
        "Yes",
        "What would you like to eat?",
        [
          [
            "Hamburger",
            "I will order hamburger for you!"
          ],
          [
            "Pizza",
            "Would you like pizza with mushrooms?",
            [
              [
                "Yes",
                "Ok, I will order the best pizza for you"
              ],
              [
                "No",
                "No? Stay hungry then"
              ]
            ]
          ]
        ]
      ],
      [
        "No",
        "Call me when you're hungry."
      ]
    ]
  ],
  [
    "Travel",
    "Would you like to travel?",
    [
      [
        "Yes",
        "Europe or Asia?",
        [
          [
            "Europe",
            "Go to Paris!"
          ],
          [
            "Asia",
            "East or West?",
            [
              [
                "East",
                "Go to China!"
              ],
              [
                "West",
                "Go to Turkey!"
              ]
            ]
          ]
        ]
      ],
      [
        "No",
        "Stay at home."
      ]
    ]
  ]
]


