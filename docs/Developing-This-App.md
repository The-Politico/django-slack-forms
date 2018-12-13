# Developing This App

## Running a Development Server

1. Move into example directory and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv run python manage.py runserver
  ```

2. In a separate terminal, start an ngrok tunnel. (If you're using the free version of ngrok don't include the `subdomain` argument.)
  ```
  $ ngrok http [YOUR_PORT_NUMBER] --subdomain=[YOUR_NGROK_SUBDOMAIN]
  ```

3. If there isn't one already, set up an app on Slack (See [Setting Up Your Slack App](/setting-up-your-slack-app)). Set the interactive `request_url` and slash command URLs to your ngrok HTTPS tunnel URL displayed in your terminal. It should be `https://[YOUR_NGROK_SUBDOMAIN].ngrok.io`.

4. If you want to develop the manual form trigger make a new slash command and set the URL to `https://[YOUR_NGROK_SUBDOMAIN].ngrok.io/test-manual/`.

## Setting Up a PostgreSQL Database

1. Run the make command to setup a fresh database.

  ```
  $ make database
  ```

2. Add a connection URL to the `.env` file.

  ```
  DATABASE_URL="postgres://localhost:5432/slackforms"
  ```

3. Run migrations from the example app.

  ```
  $ cd example
  $ pipenv run python manage.py migrate
  ```
4. Load the fixture form into your database (optional).
  ```
  $ pipenv run python manage.py loaddata exampleapp/fixtures.json
  ```

## Routes Available In Development App
- `/`: The root of Slack Forms. Used as the URL provided to Slack as the `request_url` and the URL for every slash command.
- `/callback/`: The callback route for Slack Forms. Used as a `response_url` for POST requests sent to endpoints in order to provide feedback.
- `/admin/`: The Django admin.
- `/api/test/`: A test API endpoint for GET, POST, and PUT requests used in the example form found in the `fixtures.json`.
- `/api/options/`: A test set of options for a field used in the example form found in the `fixtures.json`.
- `/test-manual/`: A test endpoint that triggers a manual form trigger if connected to a slash command.
