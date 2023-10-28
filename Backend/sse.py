import pandas as pd
import json
import global_var
import time

# from gevent.pywsgi import WSGIServer
from flask_socketio import SocketIO
from threading import Lock
import configparser
from flask import Flask, Response
from flask_cors import CORS

# from gevent import monkey
# monkey.patch_all()

thread = None
thread_lock = Lock()

config = configparser.ConfigParser()
config.read("config.cfg")
app = Flask(__name__)
app.config["SECRET_KEY"] = config["flask"]["secret_key"]
app.config["JWT_SECRET_KEY"] = config["flask"]["jwt_secret_key"]
socketio = SocketIO(app, cors_allowed_origins="*")
# jwt = JWTManager(app)

api_v1_cors_config = {
    "origins": [
        "http://localhost:8080",
        "http://10.29.51.15:8080",
        "http://10.29.51.15:3000",
        "http://172.20.15.5:3000",
        "http://10.29.90.96:8080",
        "http://172.20.32.32:8080",
    ],
    "methods": ["GET", "POST"],
    "allow_headers": ["Authorization", "Content-Type"],
}

CORS(
    app,
    resources={
        r"/api/v1/*": api_v1_cors_config,
    },
)


def background_thread():
    print("Getting Values")
    while True:
        df = pd.read_csv("./current_stock_counter.csv")
        end_loop = False
        current_values: list = []
        temp_values: dict = {}
        current_values: list = []
        temp_values: dict = {}
        for count, stocks in enumerate(global_var.all_stocks):
            try:
                data = global_var.df[stocks][df.iat[0, 0]]
            except KeyError:
                end_loop = True
                break
            temp_values["id"] = count + 1
            temp_values["name"] = stocks
            temp_values["price"] = str(data)
            current_values.append(temp_values)
            temp_values = {}
        if end_loop:
            data = {"data": f"{not end_loop}"}
            socketio.emit("new_data", {"data": False})
            socketio.sleep(30)
        else:
            df.iat[0, 0] += 1
            df.to_csv("./current_stock_counter.csv", index=False)
            socketio.emit("new_data", current_values)
            socketio.sleep(30)

        # for count, stocks in enumerate(global_var.all_stocks):
        #     try:
        #         data = global_var.df[stocks][df.iat[0, 0]]
        #     except KeyError:
        #         end_loop = True
        #         break
        #     temp_values["id"] = count + 1
        #     temp_values["name"] = stocks
        #     temp_values["price"] = str(data)
        #     current_values.append(temp_values)
        #     temp_values = {}
        #     data = json.dumps(current_values)
        #     print(data)
        #     if end_loop:
        #         print(end_loop, "inside end loop")
        #         data = {"data": f"{not end_loop}"}
        #         # yield f"data: {data}\n\n"
        #         socketio.emit('new_data', {'data': False})
        #         socketio.sleep(5)
        #     else:
        #         df.iat[0, 0] += 1
        #         df.to_csv("./current_stock_counter.csv", index=False)
        #         # yield f"data: {data}\n\n"
        #         socketio.emit('new_data', data)
        #         socketio.sleep(5)


@socketio.on("connect")
def connect():
    global thread
    print("client connected")
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

    # @app.route("/api/v1/listenforstocks")
    # def listen():
    #     df = pd.read_csv("./current_stock_counter.csv")

    #     def respond_to_client():
    #         end_loop = False
    #         while True:
    #             current_values: list = []
    #             temp_values: dict = {}
    #             for count, stocks in enumerate(global_var.all_stocks):
    #                 try:
    #                     data = global_var.df[stocks][df.iat[0, 0]]
    #                 except KeyError:
    #                     end_loop = True
    #                     break
    #                 temp_values["id"] = count + 1
    #                 temp_values["name"] = stocks
    #                 temp_values["price"] = str(data)
    #                 current_values.append(temp_values)
    #                 temp_values = {}
    #             data = json.dumps(current_values)
    #             if end_loop:
    #                 data = {"data": f"{not end_loop}"}
    #                 yield f"data: {data}\n\n"
    #                 time.sleep(30)
    #             else:
    #                 df.iat[0, 0] += 1
    #                 df.to_csv("./current_stock_counter.csv", index=False)
    #                 yield f"data: {data}\n\n"
    #                 time.sleep(30)
    #     return Response(respond_to_client(), mimetype='text/event-stream')


if __name__ == "__main__":
    # app.run(debug=True, threaded=True)
    # http_server = WSGIServer(("0.0.0.0", 5001), app)
    # http_server.serve_forever()
    socketio.run(app, host="0.0.0.0", port=5050)
