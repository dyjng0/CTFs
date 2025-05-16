from flask import Flask, request, jsonify, render_template_string, make_response
from random import choice

app = Flask(__name__)

messages = [
    {
        "role": "system",
        "message": "Nyawwo to r2gpt! Type a message below to chat with the me, owo!",
    }
]

responses = [
    "owo",
    "uwu",
    "gyatt!",
    "nyaa~",
    "hewwo",
    "DOM CLOBBERING?!?!",
    "I love pickles!!!",
    "hehe pp (prototype pollution)",
]


def render_message(resp: str) -> str:
    return f"""
    <div class="message-container {resp['role']}">
        <div class="role">{resp['role']}:</div>
        <div class="message">{resp['message']}</div>
    </div>
    """


@app.get("/")
def index():
    messages_html = "\n".join([render_message(msg) for msg in messages])

    resp = make_response(
        """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>r2gpt</title>
        <link rel="stylesheet" href="/styles.css">
        <script src="/scripts.js"></script>
    </head>
    <body>
        <h1>r2gpt</h1>
        <hr>
        <div class="messages">
            %s
        </div>
        <div class="new-message">      
            <input id="message" type="text" placeholder="Type a message...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </body>
    """
        % messages_html
    )
    resp.mimetype = "text/html"

    return resp


@app.get("/styles.css")
def styles():
    style = """
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #74AA9C;
            color: black;
        }
        h1 {
            text-align: center;
        }
        hr {
            margin: 0.5rem 0;
            border: 1px solid black;
        }
        .messages {
            display: flex;
            flex-direction: column;
            gap: 10px;
            padding: 10px;
            border: none;
            margin: 10px;
            overflow-y: auto;
        }
        .message-container {
            gap: 10px;
            border: 1px solid black;
            padding: 10px;
            border-radius: 5px;
        }
        .user {
            align-self: flex-end;
            float: right;
        }
        .system {
            align-self: flex-start;
            float: left;
        }
        .message {
            display: inline;
        }
        .role {
            display: inline;
            font-weight: bold;
        }
        .new-message {
            display: flex;
            gap: 10px;
            margin: 20px;
            border: 1px solid black;
            padding: 10px;
            border-radius: 5px;
        }
        input[type="text"] {
            flex: 1;
            padding: 5px;
            border: none;
            background-color: #74AA9C;
        }
        input::placeholder
        {
            color: black;
            opacity: 1;
        }
        input:focus {
            outline: none;
        }
        button {
            padding: 5px 10px;
            background-color: #74AA9C;
            cursor: pointer;
            border: 1px solid black;
            border-radius: 5px;
        }
        button:hover {
            background-color: #5C8D89;
        }
    """

    resp = make_response(style)
    resp.mimetype = "text/css"

    return resp


@app.get("/scripts.js")
def scripts():
    script = """
    function sendMessage() {
        var message = document.getElementById('message').value;
        fetch('/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
            }),
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            if (data.status === 'ok') {
                document.getElementById('message').value = '';
                location.reload();
            }
            else {
                alert('Error: ' + data.error);
            }
        });
    }

    window.onkeydown = function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    };
    """

    resp = make_response(script)
    resp.mimetype = "application/javascript"

    return resp


@app.post("/message")
def message():
    msg = request.json.get("message", "")
    try:
        # I hope users don't send messages of {{7*7}} ...
        msg = render_template_string(msg)

        messages.append(
            {
                "role": "user",
                "message": msg,
            }
        )
        messages.append(
            {
                "role": "system",
                "message": choice(responses),
            }
        )

        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
