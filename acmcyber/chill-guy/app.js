const express = require('express');
const cookieParser = require('cookie-parser');
const crypto = require('crypto');
const path = require('path');
const fs = require('fs');

const port = process.env.PORT ?? 3000;
const chillpw = process.env.CHILLPW ?? crypto.randomUUID();
const flag = process.env.FLAG ?? 'cyber{owo_uwu}';

const redirectMsg = (res, msg) => res
  .status(302)
  .location(`/?msg=${encodeURIComponent(msg)}`);

const users = new Map();

users.set('chill-guy', {
  name: 'chill-guy',
  password: chillpw,
  note: flag
});

app = express();
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser(crypto.randomBytes(16)));

// no request should take more than 1 second
app.use((req, res, next) => {
  setTimeout(() => res.end(), 1000);
  next();
});

app.post('/register', (req, res) => {
  const { username, password, note } = req.body;

  if (users.has(username)) {
    redirectMsg(res, 'err: user already exists');
  } else {
    users.set(username, {
      name: username, password, note
    });
    redirectMsg(res, 'user created!');
  }
  res.end();
});

app.post('/view', (req, res) => {
  const { username, password } = req.body;

  if (users.has(username)) {
    const user = users.get(username);
    if (user.password !== password) {
      redirectMsg(res, 'err: incorrect password owo');
    }
    const template = fs.readFileSync(path.join(__dirname, 'site/view.html')).toString();
    res.send(template.replaceAll('$USERNAME$', username).replaceAll('$NOTE$', user.note));
  } else {
    redirectMsg(res, 'err: user not found');
  }
  res.end();
});

app.use('/', express.static(path.join(__dirname, 'site')));

app.listen(port, () => {
  console.log(`Listening on http://localhost:${port}`);
});