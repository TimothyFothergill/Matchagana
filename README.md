# Matchagana
Matchagana - Match Kana to their Romaji equivalents

A simple matching game, you are awarded 100 points for every correct pair and lose 50 points for every incorrect pair.

The game is written in Python, using the Flask web framework to display the content dynamically. This game has been deployed to Heroku at http://matchagana.herokuapp.com/. Go check it out! Two game modes: Match-a-Hiragana and Match-a-Katakana

# Installation
`docker build -t matchagana-app .`
`docker-compose up` use `-d` flag for detached mode.
You will also need to set up a local environment variable for `APP_SECRET_KEY`.
