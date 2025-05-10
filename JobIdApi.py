import time
from flask import Flask, jsonify, request, render_template_string
import requests
import threading

app = Flask(__name__)
SERVERLISTS = []
place_id = 16732694052
min_players = 8
max_players = 15

def getData():
    try:
        response = requests.get(
            url=f"https://games.roblox.com/v1/games/{place_id}/servers/Public?sortOrder=Dsc&limit=100"
        )
        if response:
            return response.json()
        else:
            print("Failed getting data from API")
    except Exception as e:
        print(f"Error in getData(): {e}")


def sortData(response):
    global SERVERLISTS
    serverList = []
    if response:
        try:
            for server in response.get("data", []):
                if min_players <= server.get("playing") <= max_players:
                    serverList.append(server)
            SERVERLISTS = serverList
            print(SERVERLISTS)
        except Exception as e:
            print(f"Error in sortData(): {e}")

@app.route('/')
def home():
    return render_template_string('''
           <!DOCTYPE html>
           <html lang="en">
           <head>
               <meta charset="UTF-8">
               <meta name="viewport" content="width=device-width, initial-scale=1.0">
               <title>Welcome</title>
               <style>
                   body {
                       font-family: Arial, sans-serif;
                       display: flex;
                       justify-content: center;
                       align-items: center;
                       height: 100vh;
                       margin: 0;
                       background-color: #f0f0f0;
                   }
                   .container {
                       text-align: center;
                   }
                   .button {
                       background-color: #007bff;
                       color: white;
                       padding: 15px 32px;
                       font-size: 16px;
                       border: none;
                       border-radius: 5px;
                       cursor: pointer;
                       text-decoration: none;
                       margin: 10px;
                       display: inline-block;
                       transition: background-color 0.3s ease;
                   }
                   .button:hover {
                       background-color: #0056b3;
                   }
               </style>
           </head>
           <body>
               <div class="container">
                   <h1>Welcome to Versitile</h1>
                   <p>Choose a link to proceed:</p>
                   <a href="https://discord.gg/96Z3MrMMRx" class="button">Join Discord</a>
                   <a href="https://versitile.mysellauth.com" class="button">Sell Auth</a>
               </div>
           </body>
           </html>
       ''')

@app.route('/servers', methods=['POST'])
def get_servers():
    data = request.json
    if not data:
        return jsonify({"message": "Failed to get data from the request."})
    job_id = data.get("JOBID")
    if not job_id:
        return jsonify({"message": "Must include JSON body with 'JOBID' key."}), 400

    for job in SERVERLISTS:
        if job["id"] != job_id:
            id = job["id"]
            SERVERLISTS.remove(job)
            return jsonify({"id": id})

    return jsonify({"message": "All servers matched your job ID."})


def loop():
    while True:
        response = getData()
        sortData(response)
        time.sleep(30)


if __name__ == '__main__':
    print("🚀 Flask server running on port 8080")
    threading.Thread(target=loop, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)
