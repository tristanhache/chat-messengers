document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    const username = document.querySelector('#username').textContent;

    // Function to add a message to the chat
    function addMessage(username, message) {
        const ul = document.querySelector('#messages');
        const li = document.createElement('li');
        li.innerHTML = `<strong>${username}:</strong> ${message}`;
        ul.appendChild(li);
    }

    // Function to send a message
    function sendMessage() {
        const messageInput = document.querySelector('#message-input');
        const message = messageInput.value.trim();

        if (message !== '') {
            socket.emit('message', { message: message });
            messageInput.value = '';
        }
    }

    // Event listener for sending messages
    document.querySelector('#send-button').addEventListener('click', () => {
        sendMessage();
    });

    // Event listener for pressing Enter to send a message
    document.querySelector('#message-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Event listener for receiving messages
    socket.on('message', (data) => {
        const { user, message } = data;
        addMessage(user, message);
    });

    // Event listener for updating the user list
    socket.on('update_user_list', (data) => {
        const userList = data.users;
        console.log(userList); // You can update the user list UI here
    });

    // Event listener for initial messages
    socket.on('connect', () => {
        socket.emit('connect');
    });

    // Event listener for private messages
    socket.on('private_message', (data) => {
        // Handle private messages if needed
    });
});
