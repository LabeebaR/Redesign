/* Impex Studios — site scripts (no dependencies) */
(function () {
  document.documentElement.classList.add('js');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Mobile nav */
  var toggle = document.querySelector('.nav-toggle');
  var links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      links.classList.toggle('open', !open);
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { toggle.setAttribute('aria-expanded', 'false'); links.classList.remove('open'); }
    });
  }

  /* Live call demo */
  var call = document.querySelector('[data-call]');
  if (call) {
    var lines = call.querySelectorAll('.transcript li');
    var chips = call.querySelectorAll('.chip');
    if (reduce) {
      lines.forEach(function (l) { l.classList.add('on'); });
      chips.forEach(function (c) { c.classList.add('done'); });
    } else {
      var run = function () {
        lines.forEach(function (l) { l.classList.remove('on'); });
        chips.forEach(function (c) { c.classList.remove('done'); });
        var t = 400;
        lines.forEach(function (l) {
          setTimeout(function () { l.classList.add('on'); }, t);
          t += 600 + l.textContent.length * 26;
        });
        chips.forEach(function (c, i) { setTimeout(function () { c.classList.add('done'); }, t + i * 450); });
        setTimeout(run, t + chips.length * 450 + 5200);
      };
      if ('IntersectionObserver' in window) {
        var started = false;
        new IntersectionObserver(function (es) {
          if (!started && es[0].isIntersecting) { started = true; run(); }
        }, { threshold: 0, rootMargin: '0px 0px -20% 0px' }).observe(call);
      } else { run(); }
    }
  }

  var money = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };

  /* Missed-call calculator */
  var calc = document.querySelector('[data-calc]');
  if (calc) {
    var upd = function () {
      var calls = +calc.querySelector('#calls').value;
      var rate = +calc.querySelector('#rate').value;
      var value = +calc.querySelector('#value').value;
      calc.querySelector('[for=calls] output').textContent = calls;
      calc.querySelector('[for=rate] output').textContent = rate + '%';
      calc.querySelector('[for=value] output').textContent = money(value);
      var monthly = calls * 4.33 * (rate / 100) * value;
      calc.querySelector('[data-monthly]').textContent = money(monthly);
      calc.querySelector('[data-yearly]').textContent = money(monthly * 12);
    };
    calc.addEventListener('input', upd); upd();
  }

  /* Investment estimator */
  var est = document.querySelector('[data-est]');
  if (est) {
    var updE = function () {
      var pkg = est.querySelector('input[name=pkg]:checked');
      var total = +pkg.value;
      var addons = [];
      est.querySelectorAll('input[name=addon]:checked').forEach(function (a) { total += +a.value; addons.push(a.dataset.label); });
      est.querySelector('[data-total]').textContent = money(total);
      est.querySelector('[data-deposit]').textContent = money(total / 2);
      est.querySelector('[data-pkgname]').textContent = pkg.dataset.label;
      var q = new URLSearchParams({ package: pkg.dataset.label, estimate: total });
      if (addons.length) q.set('addons', addons.join(', '));
      est.querySelector('[data-lock]').href = '/free-growth-plan/?' + q.toString();
    };
    est.addEventListener('change', updE); updE();
  }

  /* Prefill lead form from estimator */
  var params = new URLSearchParams(location.search);
  var msg = document.querySelector('form[data-lead] textarea[name=message]');
  if (msg && params.get('package')) {
    msg.value = 'Interested in: ' + params.get('package') +
      (params.get('addons') ? ' + ' + params.get('addons') : '') +
      (params.get('estimate') ? ' (estimate $' + params.get('estimate') + ')' : '') + '\n\n';
  }

  /* Lead forms -> /api/contact (Cloudflare Pages Function) */
  document.querySelectorAll('form[data-lead]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = form.querySelector('.form-status');
      var btn = form.querySelector('button[type=submit]');
      var label = btn.textContent;
      btn.disabled = true; btn.textContent = 'Sending…';
      status.className = 'form-status'; status.textContent = '';
      var fd = new FormData(form);
      var data = {};
      fd.forEach(function (v, k) { data[k] = data[k] ? data[k] + ', ' + v : v; });
      data.page = location.pathname;
      fetch(form.action, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (!res.ok) throw new Error(res.j && res.j.error);
          if (window.gtag) window.gtag('event', 'generate_lead', { form: form.dataset.lead });
          location.href = '/thanks/';
        })
        .catch(function (err) {
          status.className = 'form-status err';
          status.textContent = (err && err.message ? err.message + ' ' : '') + 'Your message wasn\u2019t sent. Call or text +1 (289) 608-9883, or email contact@impexstudios.com.';
          btn.disabled = false; btn.textContent = label;
        });
    });
  });

  var y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();
})();
