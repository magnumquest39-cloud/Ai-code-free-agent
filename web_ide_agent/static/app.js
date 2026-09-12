(function(){
  const form = document.getElementById('form');
  const input = document.getElementById('input');
  const messages = document.getElementById('messages');

  function append(role, text){
    const el = document.createElement('div');
    el.className = 'msg ' + (role === 'user' ? 'user' : 'bot');
    el.textContent = text;
    messages.appendChild(el);
    messages.scrollTop = messages.scrollHeight;
  }

  form.addEventListener('submit', async (ev) =>{
    ev.preventDefault();
    const text = input.value.trim();
    if(!text) return;
    append('user', text);
    input.value = '';

    try{
      const res = await fetch('/api/chat',{
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({message: text})
      });
      if(!res.ok){
        const err = await res.json();
        append('bot', 'Error: ' + (err.detail || res.statusText));
        return;
      }
      const data = await res.json();
      append('bot', data.reply || '(no reply)');
    }catch(e){
      append('bot', 'Network error: ' + e.message);
    }
  });

})();
