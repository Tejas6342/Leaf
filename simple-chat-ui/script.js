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
    messages: [{ sender: 'bot', text: 'Hey Noah here — what are you working on?' }],
  },
  {
    id: 4,
    name: 'Emma',
    messages: [{ sender: 'bot', text: 'Hi! Want to share an update?' }],
  },
  {
    id: 5,
    name: 'Liam',
    messages: [{ sender: 'bot', text: 'Hello 👋 How is your day going?' }],
  },
  {
    id: 6,
    name: 'Sophia',
    messages: [{ sender: 'bot', text: 'Hi! Tell me what you need help with.' }],
  },
  {
    id: 7,
    name: 'Ethan',
    messages: [{ sender: 'bot', text: 'Hey, I am listening.' }],
  },
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
  const cleanedText = text.replace(/\s+/g, ' ').trim();
  const shortText =
    cleanedText.length > 80 ? `${cleanedText.slice(0, 80).trimEnd()}...` : cleanedText;

  if (lower.includes('hi') || lower.includes('hello')) {
    return 'Hello! 👋';
  }
  if (lower.includes('help')) {
    return 'Sure, I can help. What do you need?';
  }
  if (lower.includes('bye')) {
    return 'Bye! Talk soon.';
  }
  if (lower.includes('?')) {
    return `Good question about "${shortText}". Share a bit more detail and I will answer clearly.`;
  }
  if (
    lower.includes('error') ||
    lower.includes('bug') ||
    lower.includes('issue') ||
    lower.includes('problem')
  ) {
    return `I understand there is an issue: "${shortText}". What exactly is failing right now?`;
  }
  if (lower.includes('thanks') || lower.includes('thank you')) {
    return 'You are welcome! If needed, send the next detail and I will continue.';
  }
  if (lower.includes('project') || lower.includes('work') || lower.includes('task')) {
    return `Got it — "${shortText}" sounds important. What is your next step on it?`;
  }

  return `Got it: "${shortText}". Tell me one more detail so I can respond better.`;
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
