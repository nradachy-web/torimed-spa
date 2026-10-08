/* ToriMed Spa: menu tabs, the "your visit" picker and the booking request form. */
(function () {
  'use strict';

  // Site settings. Booking requests are emailed through Web3Forms once formKey is set.
  // Until then the form copies the request so the client can paste it into an Instagram message.
  var SITE = {
    formKey: '',
    instagram: 'torimed.spa'
  };

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  var ICON_PLUS = '<svg class="i-plus" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>';
  var ICON_CHECK = '<svg class="i-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
  var ICON_X = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';

  function minutesLabel(min) {
    var h = Math.floor(min / 60), m = min % 60;
    if (!h) return m + ' min';
    return h + ' h' + (m ? ' ' + m + ' min' : '');
  }

  /* Header: solid once the page has scrolled, and the phone menu. */
  var header = $('.site-header');
  var onScroll = function () { header.classList.toggle('is-solid', window.scrollY > 24); };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  var menuBtn = $('.menu-btn');
  var nav = $('#nav');
  function closeNav() { nav.classList.remove('is-open'); menuBtn.setAttribute('aria-expanded', 'false'); }
  menuBtn.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    menuBtn.setAttribute('aria-expanded', String(open));
    if (open) header.classList.add('is-solid'); else onScroll();
  });
  nav.addEventListener('click', function (e) { if (e.target.closest('a')) closeNav(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeNav(); });

  /* Category tabs. Without JavaScript every panel simply stays visible. */
  var tabs = $$('.cat');
  var panels = $$('.menu__panel');
  function selectTab(tab, focus) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
    });
    panels.forEach(function (p) {
      var on = p.id === tab.getAttribute('aria-controls');
      p.hidden = !on;
      p.classList.toggle('is-entering', on);
    });
    if (focus) tab.focus();
  }
  tabs.forEach(function (tab, i) {
    tab.addEventListener('click', function () { selectTab(tab); });
    tab.addEventListener('keydown', function (e) {
      var to = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') to = tabs[(i + 1) % tabs.length];
      if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') to = tabs[(i - 1 + tabs.length) % tabs.length];
      if (e.key === 'Home') to = tabs[0];
      if (e.key === 'End') to = tabs[tabs.length - 1];
      if (to) { e.preventDefault(); selectTab(to, true); }
    });
  });
  if (tabs.length) {
    panels.forEach(function (p, i) { p.hidden = i !== 0; });
  }

  /* Your visit: services added from the menu. */
  var services = {};
  var chosen = [];
  $$('.svc').forEach(function (row) {
    var id = row.dataset.id;
    var name = $('.svc__name', row).textContent.trim();
    services[id] = { id: id, name: name, price: Number(row.dataset.price), min: Number(row.dataset.min), row: row };
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'svc__add';
    btn.setAttribute('aria-pressed', 'false');
    btn.setAttribute('aria-label', 'Add ' + name + ' to your visit');
    btn.innerHTML = ICON_PLUS + ICON_CHECK;
    btn.addEventListener('click', function () { toggle(id); });
    row.appendChild(btn);
    services[id].btn = btn;
  });

  function toggle(id) {
    var at = chosen.indexOf(id);
    if (at === -1) chosen.push(id); else chosen.splice(at, 1);
    render();
  }

  var dock = $('#dock');
  var dockSum = $('#dock-sum');
  var dockCount = $('#dock-count');
  var dockDetail = $('#dock-detail');
  var dockBtn = $('#dock-btn');
  var picked = $('#picked');
  var pickedSum = $('#picked-sum');
  var generalField = $('#general-field');
  var pickLink = $('#pick-link');

  function totals() {
    return chosen.reduce(function (t, id) {
      t.price += services[id].price; t.min += services[id].min; return t;
    }, { price: 0, min: 0 });
  }

  function render() {
    Object.keys(services).forEach(function (id) {
      var s = services[id], on = chosen.indexOf(id) !== -1;
      s.btn.setAttribute('aria-pressed', String(on));
      s.btn.setAttribute('aria-label', (on ? 'Remove ' : 'Add ') + s.name + (on ? ' from your visit' : ' to your visit'));
      s.row.classList.toggle('is-added', on);
    });

    var n = chosen.length, t = totals();
    var has = n > 0;
    dock.classList.toggle('has-sum', has);
    dockSum.hidden = !has;
    dockCount.textContent = n + (n === 1 ? ' service' : ' services');
    dockDetail.textContent = '$' + t.price + ', about ' + minutesLabel(t.min);
    dockBtn.textContent = has ? 'Book this visit' : 'Book an appointment';

    picked.hidden = !has;
    pickedSum.hidden = !has;
    generalField.hidden = has;
    pickLink.textContent = has ? 'Add more from the menu' : 'Pick exact services from the menu';
    picked.innerHTML = '';
    chosen.forEach(function (id) {
      var s = services[id];
      var li = document.createElement('li');
      li.appendChild(document.createTextNode(s.name + ', $' + s.price));
      var rm = document.createElement('button');
      rm.type = 'button';
      rm.setAttribute('aria-label', 'Remove ' + s.name);
      rm.innerHTML = ICON_X;
      rm.addEventListener('click', function () { toggle(id); });
      li.appendChild(rm);
      picked.appendChild(li);
    });
    pickedSum.innerHTML = has ? '<strong>Total $' + t.price + '</strong>, about ' + minutesLabel(t.min) + '.' : '';
    updateDock();
  }

  /* The dock shows after the hero and steps aside while the booking form is on screen. */
  var hero = $('.hero');
  var book = $('#book');
  var pastHero = false, atBook = false;
  function updateDock() {
    var show = pastHero && !atBook;
    dock.hidden = false;
    dock.classList.toggle('is-in', show);
    dock.setAttribute('aria-hidden', String(!show));
    $$('a', dock).forEach(function (a) { a.tabIndex = show ? 0 : -1; });
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      pastHero = !entries[0].isIntersecting; updateDock();
    }, { threshold: 0.25 }).observe(hero);
    new IntersectionObserver(function (entries) {
      atBook = entries[0].isIntersecting; updateDock();
    }, { threshold: 0.08 }).observe(book);
  }

  /* Booking request form. */
  var form = $('#book-form');
  var status = $('#form-status');
  var sendBtn = $('#send-btn');
  var sendNote = $('#send-note');
  var day = $('#f-day');

  var now = new Date();
  var iso = function (d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); };
  day.min = iso(now);

  if (!SITE.formKey) {
    sendBtn.textContent = 'Copy request for Instagram';
    sendNote.textContent = 'This copies your request so you can paste it into a message to Tori on Instagram.';
  }

  function requestText(data) {
    var t = totals();
    var lines = ['Hi Tori, I would like to book an appointment.'];
    if (chosen.length) {
      lines.push('Services: ' + chosen.map(function (id) { return services[id].name + ' ($' + services[id].price + ')'; }).join(', '));
      lines.push('Total: $' + t.price + ', about ' + minutesLabel(t.min));
    } else if (data.service_type) {
      lines.push('Service: ' + data.service_type);
    }
    var when = new Date(data.preferred_day + 'T12:00:00');
    lines.push('Preferred day: ' + when.toLocaleDateString('en-CA', { weekday: 'long', month: 'long', day: 'numeric' }) + ', ' + String(data.time_of_day).toLowerCase());
    lines.push('Name: ' + data.name);
    lines.push('Mobile: ' + data.phone);
    if (data.email) lines.push('Email: ' + data.email);
    if (data.notes) lines.push('Notes: ' + data.notes);
    return lines.join('\n');
  }

  function show(kind, html) {
    status.className = 'form__status' + (kind === 'error' ? ' is-error' : '');
    status.innerHTML = html;
    status.hidden = false;
    status.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }

  var igUrl = 'https://ig.me/m/' + SITE.instagram;
  var igButton = '<a class="btn btn--coal" href="' + igUrl + '" target="_blank" rel="noopener">Open Instagram</a>';

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!chosen.length && !form.service_type.value) {
      form.service_type.setCustomValidity('Choose a service type, or pick services from the menu.');
    } else {
      form.service_type.setCustomValidity('');
    }
    if (!form.reportValidity()) return;

    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = String(v).trim(); });
    if (data.botcheck) return;
    var text = requestText(data);

    if (!SITE.formKey) {
      var done = function (copied) {
        show('ok', '<h3>' + (copied ? 'Request copied' : 'Your request') + '</h3>' +
          '<p>' + (copied ? 'Paste it into a message to Tori and she will confirm your time.' : 'Copy the text below into a message to Tori.') + '</p>' +
          (copied ? '' : '<p style="white-space:pre-line">' + text.replace(/</g, '&lt;') + '</p>') + igButton);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
      } else { done(false); }
      return;
    }

    sendBtn.disabled = true;
    sendBtn.textContent = 'Sending';
    var t = totals();
    fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        access_key: SITE.formKey,
        subject: 'Booking request from ' + data.name,
        from_name: 'ToriMed Spa website',
        name: data.name,
        phone: data.phone,
        email: data.email,
        services: chosen.length ? chosen.map(function (id) { return services[id].name; }).join(', ') : data.service_type,
        total: chosen.length ? '$' + t.price + ', about ' + minutesLabel(t.min) : '',
        preferred_day: data.preferred_day,
        time_of_day: data.time_of_day,
        notes: data.notes,
        message: text
      })
    }).then(function (r) { return r.json(); }).then(function (j) {
      if (!j || !j.success) throw new Error('not sent');
      form.reset();
      chosen = [];
      render();
      show('ok', '<h3>Booking request sent</h3><p>Tori will reply to confirm your appointment time.</p>');
    }).catch(function () {
      show('error', '<h3>That did not send</h3><p>Your request was not delivered. Try again, or message Tori on Instagram.</p>' + igButton);
    }).then(function () {
      sendBtn.disabled = false;
      sendBtn.textContent = 'Send booking request';
    });
  });
  form.service_type.addEventListener('change', function () { form.service_type.setCustomValidity(''); });

  render();
})();
