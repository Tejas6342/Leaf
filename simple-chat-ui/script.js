const chats = [
  {
    id: 1,
    name: 'Alex',
    messages: [
      { sender: 'bot', text: 'Hey! Need anything?' },
      { sender: 'user', text: 'Just testing this chat app.' },
    ],
  },
  {
    id: 2,
    name: 'Mia',
    messages: [{ sender: 'bot', text: 'Hi there 👋' }],
  },
  {
    id: 3,
    name: 'Noah',
    messages: [{ sender: 'bot', text: 'Ready for a quick chat?' }],
  },
];

const localResponses = [
  'Sounds good to me!',
  'Nice — tell me more.',
  'Okay, I understand.',
  'That is interesting 👀',
  'Can you explain a bit more?',
  'Great point!',
  'I am here if you need help.',
];

let activeChatId = chats[0].id;
let callTimer;

const chatListEl = document.getElementById('chatList');
const messagesEl = document.getElementById('messages');
const activeNameEl = document.getElementById('activeName');
const activeAvatarEl = document.getElementById('activeAvatar');
const callStatusEl = document.getElementById('callStatus');
const messageForm = document.getElementById('messageForm');
const messageInput = document.getElementById('messageInput');
const audioCallBtn = document.getElementById('audioCallBtn');
const videoCallBtn = document.getElementById('videoCallBtn');
const callOverlay = document.getElementById('callOverlay');
const overlayAvatar = document.getElementById('overlayAvatar');
const overlayName = document.getElementById('overlayName');
const overlayText = document.getElementById('overlayText');
const endCallBtn = document.getElementById('endCallBtn');

function getActiveChat() {
  return chats.find((chat) => chat.id === activeChatId);
}

function toInitials(name) {
  return name
    .split(' ')
    .map((part) => part[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();
}

function renderChatList() {
  chatListEl.innerHTML = '';

  chats.forEach((chat) => {
    const item = document.createElement('button');
    item.type = 'button';
    item.className = `chat-item ${chat.id === activeChatId ? 'active' : ''}`;
    item.innerHTML = `
      <div class="avatar">${toInitials(chat.name)}</div>
      <div>
        <strong>${chat.name}</strong>
        <div class="status">${chat.messages.at(-1)?.text ?? ''}</div>
      </div>
    `;

    item.addEventListener('click', () => {
      activeChatId = chat.id;
      callStatusEl.textContent = 'Online';
      render();
    });

    chatListEl.appendChild(item);
  });
}

function renderMessages() {
  const activeChat = getActiveChat();
  messagesEl.innerHTML = '';

  activeChat.messages.forEach((message) => {
    const bubble = document.createElement('div');
    bubble.className = `msg ${message.sender}`;
    bubble.textContent = message.text;
    messagesEl.appendChild(bubble);
  });

  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function renderHeader() {
  const activeChat = getActiveChat();
  activeNameEl.textContent = activeChat.name;
  activeAvatarEl.textContent = toInitials(activeChat.name);
}

function render() {
  renderChatList();
  renderHeader();
  renderMessages();
}

function getLocalResponse(text) {
  const lower = text.toLowerCase();

  if (lower.includes('hi') || lower.includes('hello')) {
    return 'Hello! 👋';
  }
  if (lower.includes('help')) {
    return 'Sure, I can help. What do you need?';
  }
  if (lower.includes('bye')) {
    return 'Bye! Talk soon.';
  }

  const randomIndex = Math.floor(Math.random() * localResponses.length);
  return localResponses[randomIndex];
}

messageForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const text = messageInput.value.trim();

  if (!text) return;

  const activeChat = getActiveChat();
  activeChat.messages.push({ sender: 'user', text });
  render();
  messageInput.value = '';

  setTimeout(() => {
    activeChat.messages.push({ sender: 'bot', text: getLocalResponse(text) });
    render();
  }, 450);
});

function showCallingUI(type) {
  const activeChat = getActiveChat();
  overlayAvatar.textContent = toInitials(activeChat.name);
  overlayName.textContent = activeChat.name;
  overlayText.textContent = `${type} calling...`;
  callStatusEl.textContent = `${type} calling...`;
  callOverlay.classList.remove('hidden');

  clearTimeout(callTimer);
  callTimer = setTimeout(() => {
    overlayText.textContent = `${type} call connected (demo UI)`;
    callStatusEl.textContent = `On ${type.toLowerCase()} call`;
  }, 1200);
}

audioCallBtn.addEventListener('click', () => showCallingUI('Audio'));
videoCallBtn.addEventListener('click', () => showCallingUI('Video'));

endCallBtn.addEventListener('click', () => {
  clearTimeout(callTimer);
  callOverlay.classList.add('hidden');
  callStatusEl.textContent = 'Online';
});

render();
