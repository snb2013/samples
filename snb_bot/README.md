# Chat Bot API

Test application to emulate chat with bot.
Actual data should be seed before usage.

## Install

    docker-compose build

## Seed

    docker-compose up seed

## Run

    docker-compose up runserver

## Test

    docker-compose up autotests

## Usage

`http://0.0.0.0` - main page

`http://0.0.0.0/admin/` admin

`http://0.0.0.0/api/` available API

`http://0.0.0.0/api/lists/` questionnaires list

`http://0.0.0.0/api/questions/?list=[LIST_ID]` initial question of the given questionnaires list

`http://0.0.0.0/api/questions/?list=[LIST_ID]&answer=[QUESTION_ID]` - question on answer of the given questionnaires list
