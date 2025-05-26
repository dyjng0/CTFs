document.addEventListener('DOMContentLoaded', function () {
    const storedToken = localStorage.getItem('queue_token');
    const storedUserId = localStorage.getItem('queue_user_id');

    if (storedToken && storedUserId) {
        document.getElementById('join-queue-section').classList.add('hidden');
        document.getElementById('check-queue-section').classList.remove('hidden');
        document.getElementById('user-display').textContent = storedUserId;

        checkQueue(storedToken);
    }
});

document.getElementById('join-queue-btn').addEventListener('click', function () {
    const userId = document.getElementById('user_id').value;
    if (!userId) {
        showResult('Please enter your email or username to continue', 'error');
        return;
    }

    fetch('/join_queue', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_id=${encodeURIComponent(userId)}`
    })
        .then(response => response.json())
        .then(data => {
            if (data.token) {
                localStorage.setItem('queue_token', data.token);
                localStorage.setItem('queue_user_id', userId);

                document.getElementById('join-queue-section').classList.add('hidden');
                document.getElementById('check-queue-section').classList.remove('hidden');
                document.getElementById('user-display').textContent = userId;

                const waitTimeMessage = data.wait_minutes ?
                    `${data.wait_minutes} minutes` :
                    'Calculating...';


                showResult(`You are in the queue! Estimated wait time: ${waitTimeMessage}`);
                checkQueue(data.token);
            } else {
                showResult(data.error || 'Unknown error occurred', 'error');
            }
        })
        .catch(error => {
            showResult('Error: ' + error.message, 'error');
            console.error('Error:', error);
        });
});

document.getElementById('check-queue-btn').addEventListener('click', function () {
    const token = localStorage.getItem('queue_token');
    if (token) {
        checkQueue(token);
    } else {
        showResult('No queue token found. Please join the queue again.', 'error');
    }
});


document.getElementById('purchase-btn').addEventListener('click', function () {
    const token = localStorage.getItem('queue_token');

    if (!token) {
        showResult('No queue token found. Please join the queue first.', 'error');
        return;
    }

    showResult('Processing your purchase...', 'info');

    let downloadingTicket = true;

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/purchase';
    form.target = '_blank';

    const tokenInput = document.createElement('input');
    tokenInput.type = 'hidden';
    tokenInput.name = 'token';
    tokenInput.value = token;
    form.appendChild(tokenInput);

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);

    setTimeout(() => {
        fetch('/purchase?html=true', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `token=${encodeURIComponent(token)}`
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showResult(`
            <h3 style="color: #4fc3f7; margin-top: 0;">Congratulations!</h3>
            <p>${data.message}</p>
            <p style="margin-top: 20px;">Your ticket is being downloaded. If the download didn't start, <a href="/purchase" style="color: #4fc3f7;" onclick="downloadTicket(event)">click here</a>.</p>
        `, 'success');
                } else {
                    showResult(data.message || data.error || 'Unknown error occurred', 'error');
                }

                if (data.error_details || data.details) {
                    const debugSection = document.getElementById('debug-section');
                    debugSection.classList.remove('hidden');

                    const debugData = data.error_details || data.details;
                    document.getElementById('debug-output').textContent = JSON.stringify(debugData, null, 2);
                }
            })
            .catch(error => {
                showResult('Error: ' + error.message, 'error');
                console.error('Error:', error);
            });
    }, 500);
});

function downloadTicket(event) {
    event.preventDefault();
    const token = localStorage.getItem('queue_token');

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/purchase';
    form.target = '_blank';

    const tokenInput = document.createElement('input');
    tokenInput.type = 'hidden';
    tokenInput.name = 'token';
    tokenInput.value = token;
    form.appendChild(tokenInput);

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}

function checkQueue(token) {
    fetch('/check_queue', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `token=${encodeURIComponent(token)}`
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ready') {
                document.getElementById('check-queue-section').classList.add('hidden');
                document.getElementById('purchase-section').classList.remove('hidden');
                showResult(data.message || 'Your turn has arrived! You can now purchase tickets.', 'success');
            } else {
                if (data.queue_position) {
                    document.getElementById('position-display').textContent = data.queue_position.toLocaleString();
                }

                if (data.wait_minutes) {
                    const hours = Math.floor(data.wait_minutes / 60);
                    const minutes = data.wait_minutes % 60;
                    let waitTimeDisplay = "";
                    let stingerQuote = "";

                    if (data.wait_minutes > 5000) {
                        stingerQuote = Math.random() < 0.5 ?
                            "Yikes, get comfortable." :
                            "You might wanna go start graduate school or something while you wait.";
                    } else if (data.wait_minutes < 5) {
                        stingerQuote = Math.random() < 0.5 ?
                            "Woah, you're next up!" :
                            "How did you do that...?";
                    } else if (data.wait_minutes < 1) {
                        stingerQuote = "Get ready!";
                    }

                    if (hours > 24) {
                        const days = Math.floor(hours / 24);
                        const remainingHours = hours % 24;
                        waitTimeDisplay = `${data.wait_minutes.toLocaleString()} minutes (approximately ${days} days and ${remainingHours} hours)`;
                    } else if (hours > 0) {
                        waitTimeDisplay = `${data.wait_minutes.toLocaleString()} minutes (approximately ${hours} hours and ${minutes} minutes)`;
                    } else {
                        waitTimeDisplay = `${data.wait_minutes.toLocaleString()} minutes`;
                    }

                    document.getElementById('time-display').textContent = waitTimeDisplay;

                    if (stingerQuote) {
                        const quoteElem = document.createElement('p');
                        quoteElem.className = 'queue-stinger';
                        quoteElem.style.fontStyle = 'italic';
                        quoteElem.style.color = '#ffeb3b';
                        quoteElem.style.marginTop = '10px';
                        quoteElem.textContent = stingerQuote;

                        const existingStinger = document.querySelector('.queue-stinger');
                        if (existingStinger) {
                            existingStinger.textContent = stingerQuote;
                        } else {
                            document.querySelector('.queue-status').appendChild(quoteElem);
                        }
                    }
                }

                showResult(data.message || `Still waiting in queue.`);
            }

            if (data.error_details || data.details) {
                const debugSection …
