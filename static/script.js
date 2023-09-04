document.addEventListener("DOMContentLoaded", function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var username = "{{ username }}"; // Get the username from the rendered template

    // Handle login form submission
    var loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            var usernameInput = document.getElementById('username');
            var passwordInput = document.getElementById('password');
            
            // Send a login event to the server
            socket.emit('login', { username: usernameInput.value, password: passwordInput.value });
            
            // Clear the form
            usernameInput.value = '';
            passwordInput.value = '';
        });
    }

    // Handle message sending
    var messageInput = document.getElementById('message');
    var sendButton = document.getElementById('send-button');

    sendButton.addEventListener('click', function() {
        var message = messageInput.value;
        if (message.trim() !== '') {
            socket.emit('message', { message: message, user: username });
            messageInput.value = '';
        }
    });

    // Handle incoming messages
    socket.on('message', function(data) {
        var messageList = document.getElementById('messages');
        var li = document.createElement('li');
        li.textContent = data.user + ': ' + data.message;
        messageList.appendChild(li);
    });
});
