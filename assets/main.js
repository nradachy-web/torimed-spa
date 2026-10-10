/* ToriMed Spa: navigation, menu tabs, the "your visit" picker and the booking request form. */
(function () {
  'use strict';

  // Site settings. Booking requests are emailed through Web3Forms with this access key.
  // If the key is ever removed, the form falls back to copying the request for an Instagram message.
  var SITE = {
    formKey: '44fecf0f-984e-4514-b0a5-0ec33384a58e',
    instagram: 'torimed.spa',
    // Google Ads conversions: a booking request that was delivered, and a tap on "message me on Instagram".
    adsBooking: 'AW-18504296452/HyDGCOiv25cdEITQxPdE',
    adsInstagram: 'AW-18504296452/CVyGCOuv25cdEITQxPdE'
  };

  // Every service with its price and minutes, written into each page by src/build.py.
  var CATALOG = window.TORI_SERVICES || {};
  var VISIT_KEY = 'torimed-visit';

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

  /* Header: solid once the page has scrolled, the phone menu and the services list. */
  var header = $('.site-header');
  var onScroll = function () { header.classList.toggle('is-solid', window.scrollY > 24); };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  var menuBtn = $('.menu-btn');
  var nav = $('#nav');
  var group = $('.nav__group');
  var groupBtn = $('.nav__toggle');
  // Ad landing pages have no menu, only the booking button.
  if (nav) {
    var closeGroup = function () { group.classList.remove('is-open'); groupBtn.setAttribute('aria-expanded', 'false'); };
    var closeNav = function () { nav.classList.remove('is-open'); menuBtn.setAttribute('aria-expanded', 'false'); closeGroup(); onScroll(); };
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      menuBtn.setAttribute('aria-expanded', String(open));
      if (open) header.classList.add('is-solid'); else onScroll();
    });
    groupBtn.addEventListener('click', function () {
      var open = group.classList.toggle('is-open');
      groupBtn.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) closeNav(); });
    document.addEventListener('click', function (e) { if (!e.target.closest('.nav__group')) closeGroup(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeNav(); });
  }

  /* Clean addresses. Every link is a real page (/book/, /services/ and so on). When the thing a link
     points at is already on this page, scroll to it instead of leaving, and never put a "#" in the address. */
  function target(el) {
    var sel = el.getAttribute('data-scroll');
    if (!sel) return null;
    try { return document.querySelector(sel); } catch (e) { return null; }
  }
  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[data-scroll]');
    if (!link || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    var to = target(link);
    if (!to) return;
    e.preventDefault();
    to.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
  // An old link such as /#book still lands on the right spot; tidy the address once it has.
  window.addEventListener('load', function () {
    if (!location.hash || !window.history || !history.replaceState) return;
    setTimeout(function () { history.replaceState(null, '', location.pathname + location.search); }, 0);
  });

  /* Count a tap on any "message me on Instagram" link, including the one the form shows when a send fails. */
  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href^="https://ig.me/m/"]');
    if (link && window.gtag) window.gtag('event', 'conversion', { send_to: SITE.adsInstagram });
  });

  /* Category tabs on the home page. Without JavaScript every panel simply stays visible. */
  var tabs = $$('.cat');
  var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute('aria-controls')); });
  function selectTab(tab, focus) {
    tabs.forEach(function (t, i) {
      var on = t === tab;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      panels[i].hidden = !on;
      panels[i].classList.toggle('is-entering', on);
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
  panels.forEach(function (p, i) { p.hidden = i !== 0; });

  /* Your visit: services added from any price list. The choice follows the visitor from page to page. */
  var chosen = [];
  try {
    chosen = JSON.parse(sessionStorage.getItem(VISIT_KEY) || '[]').filter(function (id) { return CATALOG[id]; });
  } catch (e) { chosen = []; }
  // A service page starts with its own service in the visit, unless the visitor already has one going.
  var preselect = document.body.getAttribute('data-preselect');
  if (!chosen.length && preselect && CATALOG[preselect]) chosen = [preselect];

  function save() {
    try { sessionStorage.setItem(VISIT_KEY, JSON.stringify(chosen)); } catch (e) { /* private mode: the visit just stays on this page */ }
  }
  function has(id) { return chosen.indexOf(id) !== -1; }
  function toggle(id) {
    var at = chosen.indexOf(id);
    if (at === -1) chosen.push(id); else chosen.splice(at, 1);
    save();
    render();
  }

  var rows = [];
  $$('.svc').forEach(function (row) {
    var id = row.getAttribute('data-id');
    var s = CATALOG[id];
    if (!s) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'svc__add';
    btn.innerHTML = ICON_PLUS + ICON_CHECK;
    btn.addEventListener('click', function () { toggle(id); });
    row.appendChild(btn);
    rows.push({ id: id, row: row, btn: btn });
  });

  // Buttons such as "Book a Korean lash lift" put that service in the visit on the way to the form.
  $$('[data-add]').forEach(function (el) {
    el.addEventListener('click', function () {
      var id = el.getAttribute('data-add');
      if (!CATALOG[id]) return;
      if (!has(id)) chosen.push(id);
      save();
      render();
    });
  });

  var dock = $('#dock');
  var dockSum = $('#dock-sum');
  var dockCount = $('#dock-count');
  var dockDetail = $('#dock-detail');
  var dockBtn = $('#dock-btn');
  // Pages without a price list, such as makeup, ask about a kind of service instead.
  var pageType = document.body.getAttribute('data-service-type');
  var form = $('#book-form');
  var picked = $('#picked');
  var pickedSum = $('#picked-sum');
  var generalField = $('#general-field');
  var pickLink = $('#pick-link');

  function totals() {
    return chosen.reduce(function (t, id) {
      t.price += CATALOG[id].price; t.min += CATALOG[id].min; return t;
    }, { price: 0, min: 0 });
  }

  function render() {
    rows.forEach(function (r) {
      var on = has(r.id), name = CATALOG[r.id].name;
      r.btn.setAttribute('aria-pressed', String(on));
      r.btn.setAttribute('aria-label', (on ? 'Remove ' : 'Add ') + name + (on ? ' from your visit' : ' to your visit'));
      r.row.classList.toggle('is-added', on);
    });

    var n = chosen.length, t = totals();
    var any = n > 0;
    dock.classList.toggle('has-sum', any);
    dockSum.hidden = !any;
    dockCount.textContent = n + (n === 1 ? ' service' : ' services');
    dockDetail.textContent = '$' + t.price + ', about ' + minutesLabel(t.min);
    dockBtn.textContent = any ? 'Book this visit' : 'Book an appointment';

    if (form) {
      picked.hidden = !any;
      pickedSum.hidden = !any;
      generalField.hidden = any && !pageType;
      pickLink.textContent = any ? 'Add more from the price list' : 'Pick exact services from the price list';
      picked.innerHTML = '';
      chosen.forEach(function (id) {
        var s = CATALOG[id];
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
      pickedSum.innerHTML = any ? '<strong>Total $' + t.price + '</strong>, about ' + minutesLabel(t.min) + '.' : '';
    }
    updateDock();
  }

  // Heading to the form with a visit on screen keeps it, even if the page chose it for them.
  dockBtn.addEventListener('click', save);

  /* The dock shows after the top of the page and steps aside while the booking form is on screen. */
  var top = $('.hero') || $('.pagehead');
  var book = $('#book');
  var pastTop = false, atBook = false;
  function updateDock() {
    var show = pastTop && !atBook;
    dock.hidden = false;
    dock.classList.toggle('is-in', show);
    dock.setAttribute('aria-hidden', String(!show));
    $$('a', dock).forEach(function (a) { a.tabIndex = show ? 0 : -1; });
  }
  if ('IntersectionObserver' in window) {
    if (top) {
      new IntersectionObserver(function (entries) {
        pastTop = !entries[0].isIntersecting; updateDock();
      }, { threshold: 0.25 }).observe(top);
    }
    if (book) {
      new IntersectionObserver(function (entries) {
        atBook = entries[0].isIntersecting; updateDock();
      }, { threshold: 0.08 }).observe(book);
    }
  }

  /* Booking request form. */
  if (form) initForm();

  function initForm() {
    var status = $('#form-status');
    var sendBtn = $('#send-btn');
    var sendNote = $('#send-note');
    var day = $('#f-day');

    var now = new Date();
    var iso = function (d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); };
    day.min = iso(now);

    if (pageType) form.service_type.value = pageType;

    if (!SITE.formKey) {
      sendBtn.textContent = 'Copy request for Instagram';
      sendNote.textContent = 'This copies your request so you can paste it into a message to me on Instagram.';
    }

    function requestText(data) {
      var t = totals();
      var lines = [form.getAttribute('data-opening') || 'Hi Tori, I would like to book an appointment.'];
      if (chosen.length) {
        lines.push('Services: ' + chosen.map(function (id) { return CATALOG[id].name + ' ($' + CATALOG[id].price + ')'; }).join(', '));
        lines.push('Total: $' + t.price + ', about ' + minutesLabel(t.min));
      }
      if (data.service_type && !generalField.hidden) lines.push((chosen.length ? 'Also asking about: ' : 'Service: ') + data.service_type);
      var when = new Date(data.preferred_day + 'T12:00:00');
      lines.push((form.getAttribute('data-day-label') || 'Preferred day') + ': ' + when.toLocaleDateString('en-CA', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }) + ', ' + String(data.time_of_day).toLowerCase());
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
        form.service_type.setCustomValidity('Choose a service type, or pick services from the price list.');
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
            '<p>' + (copied ? 'Paste it into a message to me on Instagram and I will confirm your time.' : 'Copy the text below into a message to me on Instagram.') + '</p>' +
            (copied ? '' : '<p style="white-space:pre-line">' + text.replace(/</g, '&lt;') + '</p>') + igButton);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
        } else { done(false); }
        return;
      }

      var label = sendBtn.textContent;
      sendBtn.disabled = true;
      sendBtn.textContent = 'Sending';
      var t = totals();
      var services = chosen.map(function (id) { return CATALOG[id].name; });
      if (data.service_type && !generalField.hidden) services.push(data.service_type);
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
          services: services.join(', '),
          total: chosen.length ? '$' + t.price + ', about ' + minutesLabel(t.min) : '',
          day: data.preferred_day,
          time_of_day: data.time_of_day,
          notes: data.notes,
          page: location.pathname,
          message: text
        })
      }).then(function (r) { return r.json(); }).then(function (j) {
        if (!j || !j.success) throw new Error('not sent');
        if (window.gtag) {
          window.gtag('event', 'generate_lead', { form_page: location.pathname });
          window.gtag('event', 'conversion', { send_to: SITE.adsBooking });
        }
        form.reset();
        if (pageType) form.service_type.value = pageType;
        chosen = [];
        save();
        render();
        show('ok', '<h3>Request sent</h3><p>' + (form.getAttribute('data-sent') || 'I will reply to confirm your appointment time.') + '</p>');
      }).catch(function () {
        show('error', '<h3>That did not send</h3><p>Your request was not delivered. Try again, or message me on Instagram.</p>' + igButton);
      }).then(function () {
        sendBtn.disabled = false;
        sendBtn.textContent = label;
      });
    });
    form.service_type.addEventListener('change', function () { form.service_type.setCustomValidity(''); });
  }

  render();
})();
