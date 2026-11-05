/* Book online: services, open times and booking come live from Tori's Square calendar,
   through her booking desk. The page never works out a price or a time itself. */
(function () {
  var root = document.getElementById('book');
  if (!root || !root.classList.contains('live')) return;

  var desk = root.getAttribute('data-desk');
  var ads = root.getAttribute('data-ads');
  // A copy of the site served on this computer may point at a desk running here too.
  var params = new URLSearchParams(location.search);
  if (/^(127\.0\.0\.1|localhost)$/.test(location.hostname) && params.get('desk')) desk = params.get('desk');

  var el = function (id) { return document.getElementById(id); };
  var groupsEl = el('live-groups'), svcHint = el('live-svc-hint'), sumEl = el('live-sum');
  var whenEl = el('live-when'), timeHint = el('live-time-hint'), daysEl = el('live-days'), timesEl = el('live-times');
  var form = el('live-form'), go = el('live-go'), statusEl = el('live-status');

  var MAX = 4;
  var services = [], byId = {}, picked = [], days = [], day = null, slot = null, open = false;
  var ask = 0, key = null, sending = false;

  function minutes(m) {
    var h = Math.floor(m / 60), r = m % 60;
    return (h ? h + ' hr' : '') + (h && r ? ' ' : '') + (r ? r + ' min' : '');
  }
  function money(n) { return n == null ? '' : '$' + (n % 1 ? n.toFixed(2) : n); }
  function newKey() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return 'k' + Date.now().toString(36) + Math.random().toString(36).slice(2, 12) + Math.random().toString(36).slice(2, 12);
  }
  function node(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function api(path, body) {
    return fetch(desk + path, body ? { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) } : {})
      .then(function (r) { return r.json().catch(function () { return { ok: false }; }).then(function (j) { j.status = r.status; return j; }); });
  }

  // ---------------------------------------------------------------- 1. services

  function drawServices() {
    groupsEl.textContent = '';
    var groups = [];
    services.forEach(function (s) {
      var g = groups.filter(function (x) { return x.name === s.group; })[0];
      if (!g) groups.push(g = { name: s.group, list: [] });
      g.list.push(s);
    });
    groups.forEach(function (g, i) {
      var box = node('details', 'live__group');
      if (i === 0) box.open = true;
      box.appendChild(node('summary', 'live__gname', g.name));
      var list = node('div', 'live__chips');
      g.list.forEach(function (s) {
        var b = node('button', 'live__chip');
        b.type = 'button';
        b.setAttribute('data-id', s.id);
        b.setAttribute('aria-pressed', 'false');
        b.appendChild(node('span', 'live__cname', s.name));
        b.appendChild(node('span', 'live__cmeta', [money(s.price), minutes(s.minutes)].filter(Boolean).join(' · ')));
        b.addEventListener('click', function () { toggle(s.id); });
        list.appendChild(b);
      });
      box.appendChild(list);
      groupsEl.appendChild(box);
    });
    groupsEl.hidden = false;
    svcHint.textContent = 'Tap everything you would like in this visit. You can choose up to ' + MAX + '.';
  }

  function toggle(id) {
    var at = picked.indexOf(id);
    if (at >= 0) picked.splice(at, 1);
    else if (picked.length < MAX) picked.push(id);
    else { svcHint.textContent = 'That is the most for one visit online. Message me for a longer one.'; return; }
    [].forEach.call(groupsEl.querySelectorAll('.live__chip'), function (b) {
      b.setAttribute('aria-pressed', picked.indexOf(b.getAttribute('data-id')) >= 0 ? 'true' : 'false');
    });
    var chosen = picked.map(function (p) { return byId[p]; });
    if (chosen.length) {
      var total = chosen.every(function (s) { return s.price != null; }) ? chosen.reduce(function (t, s) { return t + s.price; }, 0) : null;
      var time = chosen.reduce(function (t, s) { return t + s.minutes; }, 0);
      sumEl.textContent = chosen.map(function (s) { return s.name; }).join(' + ') + ' · ' + [money(total), minutes(time)].filter(Boolean).join(' · ');
      sumEl.hidden = false;
    } else sumEl.hidden = true;
    loadTimes();
  }

  // ---------------------------------------------------------------- 2. day and time

  var wait = null;
  function loadTimes() {
    slot = null; day = null; key = null;
    setGo();
    daysEl.hidden = true; timesEl.hidden = true;
    if (!picked.length) {
      whenEl.setAttribute('data-locked', '');
      timeHint.textContent = 'Choose a service first and I will show you my open times.';
      return;
    }
    whenEl.removeAttribute('data-locked');
    timeHint.textContent = 'Finding my open times...';
    clearTimeout(wait);
    var mine = ++ask;
    wait = setTimeout(function () {
      api('/api/book/times', { services: picked.slice() }).then(function (r) {
        if (mine !== ask) return;
        if (!r.ok) { timeHint.textContent = 'I could not load my calendar just now. Please try again in a moment.'; return; }
        days = r.days || [];
        if (!days.length) { timeHint.textContent = 'Nothing open for that in the next month. Message me and I will find you a time.'; return; }
        timeHint.textContent = 'Times shown are Fredericton time.';
        drawDays();
        pickDay(days[0].date);
      }, function () {
        if (mine === ask) timeHint.textContent = 'I could not load my calendar just now. Please try again in a moment.';
      });
    }, 350);
  }

  function drawDays() {
    daysEl.textContent = '';
    days.forEach(function (d) {
      var b = node('button', 'live__day');
      b.type = 'button';
      b.setAttribute('role', 'radio');
      b.setAttribute('data-date', d.date);
      var parts = d.label.split(', ');
      b.appendChild(node('span', 'live__dname', parts[0]));
      b.appendChild(node('span', 'live__ddate', parts.slice(1).join(', ')));
      b.addEventListener('click', function () { pickDay(d.date); });
      daysEl.appendChild(b);
    });
    daysEl.hidden = false;
  }

  function pickDay(date) {
    day = days.filter(function (d) { return d.date === date; })[0];
    slot = null; key = null;
    [].forEach.call(daysEl.children, function (b) { b.setAttribute('aria-checked', b.getAttribute('data-date') === date ? 'true' : 'false'); });
    timesEl.textContent = '';
    day.times.forEach(function (t) {
      var b = node('button', 'live__time', t.label);
      b.type = 'button';
      b.setAttribute('role', 'radio');
      b.setAttribute('aria-checked', 'false');
      b.addEventListener('click', function () {
        slot = t; key = newKey();
        [].forEach.call(timesEl.children, function (x) { x.setAttribute('aria-checked', x === b ? 'true' : 'false'); });
        form.removeAttribute('data-locked');
        setGo();
      });
      timesEl.appendChild(b);
    });
    timesEl.hidden = false;
    setGo();
  }

  function setGo() {
    if (!open) { go.disabled = true; go.textContent = 'Online booking opens soon'; return; }
    go.disabled = !slot || sending;
    go.textContent = sending ? 'Booking...' : slot ? 'Book ' + day.label + ' at ' + slot.label : 'Pick a time first';
  }

  // ---------------------------------------------------------------- 3. book

  function say(text, ok) {
    statusEl.textContent = '';
    statusEl.appendChild(node('p', ok ? 'live__done-h' : '', text));
    statusEl.hidden = false;
    statusEl.classList.toggle('live__done--err', !ok);
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!open || !slot || sending) return;
    var data = new FormData(form);
    var name = String(data.get('name') || '').trim(), phone = String(data.get('phone') || '').trim();
    if (!name) { form.elements.name.focus(); say('Please add your name.'); return; }
    if (phone.replace(/\D/g, '').length < 10) { form.elements.phone.focus(); say('Please add your mobile number, with the area code.'); return; }
    sending = true; setGo(); statusEl.hidden = true;
    var when = day.label + ' at ' + slot.label;
    var what = picked.map(function (p) { return byId[p].name; }).join(' + ');
    api('/api/book', {
      services: picked.slice(), startAt: slot.startAt, key: key,
      name: name, phone: phone, email: String(data.get('email') || '').trim(), notes: String(data.get('notes') || '').trim(),
      botcheck: data.get('botcheck') ? 1 : ''
    }).then(function (r) {
      sending = false;
      if (r.ok) {
        [].forEach.call(root.querySelectorAll('.live__step'), function (s) { s.hidden = true; });
        statusEl.textContent = '';
        statusEl.classList.remove('live__done--err');
        statusEl.appendChild(node('p', 'live__done-h', 'You are booked!'));
        statusEl.appendChild(node('p', '', what + ', ' + when + '.'));
        statusEl.appendChild(node('p', '', 'I am at The Beauty Collective, 191 Main Street, Fredericton. See you then.'));
        statusEl.hidden = false;
        statusEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        if (window.gtag) {
          window.gtag('event', 'generate_lead', { form_page: location.pathname, method: 'online booking' });
          if (ads) window.gtag('event', 'conversion', { send_to: ads });
        }
        return;
      }
      setGo();
      if (r.status === 409) { say(r.error || 'Someone just took that time. Please pick another.'); loadTimes(); return; }
      say(r.error || 'That did not go through. Please try again, or message me on Instagram.');
    }, function () {
      sending = false; setGo();
      say('That did not go through. Please check your connection and try again.');
    });
  });

  // ---------------------------------------------------------------- start

  api('/api/book/services').then(function (r) {
    if (!r.ok || !r.services || !r.services.length) {
      svcHint.textContent = 'My online calendar is not available right now. Please send me a booking request instead.';
      return;
    }
    open = Boolean(r.open);
    services = r.services;
    services.forEach(function (s) { byId[s.id] = s; });
    drawServices();
    setGo();
  }, function () {
    svcHint.textContent = 'My online calendar is not available right now. Please send me a booking request instead.';
  });
})();
