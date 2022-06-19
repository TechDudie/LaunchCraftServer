from flask import Flask, request
import minecraft_launcher_lib
import json
import sys
import os

CLIENT_ID = os.getenv("CLIENT_ID")
SECRET = os.getenv("SECRET")
REDIRECT_URL = "https://launchcraft-server.herokuapp.com/redirect"

if sys.argv[1] == "replit":
  REDIRECT_URL = "https://launchcraftserver.technologydev.repl.co/redirect"

error_data = ({'Error': 'Invalid Authenication Code'}, 400, {'Content-Type': 'application/json'})

app = Flask("app")

@app.route('/')
def root():
  return "<h1>LaunchCraft Authenication Server</h1>"

@app.post('/redirect')
def redirect():
  try:
    code = request.form['code']
  except:
    return error_data
  if not minecraft_launcher_lib.microsoft_account.url_contains_auth_code(f"{REDIRECT_URL}?code={code}"):
    return error_data
  data = minecraft_launcher_lib.microsoft_account.complete_login(CLIENT_ID, SECRET, REDIRECT_URL, code)
  return json.dumps({
    "username": data["name"],
    "uuid": data["id"],
    "token": data["access_token"]
  })

if sys.argv[1] == "replit":
  app.run(host='0.0.0.0', port=8080)