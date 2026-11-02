(function () {
  var stage = document.getElementById("stage"), vp = document.getElementById("viewport");
  var slides = [].slice.call(document.querySelectorAll(".slide"));
  var cur = 0, step = 0;
  var num = document.getElementById("count"), ttl = document.getElementById("ttl"), prog = document.getElementById("progi");
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  function resize() {
    if (document.body.classList.contains("overview")) return;
    var s = Math.min(vp.clientWidth / 1280, vp.clientHeight / 720);
    stage.style.transform = "scale(" + s + ")";
  }

  /* 장마다 본문 배율을 골라 무대를 채운다: 여백이 많으면 키우고 넘치면 줄인다 */
  var ZOOMS = [1.45, 1.35, 1.25, 1.15, 1.05, 1, 0.92, 0.85, 0.78, 0.7, 0.62];
  function fit() {
    var scale = stage.getBoundingClientRect().width / 1280 || 1;
    slides.forEach(function (sl) {
      var b = sl.querySelector(".body");
      if (!b || !b.children.length) return;
      if (b.querySelector(".agents,.ioscene")) { sl.dataset.fit = "1.00"; return; }
      b.style.justifyContent = "flex-start";
      var z = 1;
      for (var i = 0; i < ZOOMS.length; i++) {
        z = ZOOMS[i];
        b.style.zoom = z;
        var top = b.firstElementChild.getBoundingClientRect().top;
        var bot = 0, right = 0;
        [].forEach.call(b.children, function (c) { var r = c.getBoundingClientRect(); bot = Math.max(bot, r.bottom); });
        if (bot - top <= b.getBoundingClientRect().height + 1 && b.scrollWidth <= b.clientWidth + 1) break;
      }
      b.style.justifyContent = "";
      sl.dataset.fit = z.toFixed(2);
    });
  }

  /* 큰 숫자 세기: 정수 한 자리와 날짜처럼 숫자가 여럿인 값은 그대로 둔다 */
  var timers = [];
  function countUp(sl) {
    timers.forEach(cancelAnimationFrame); timers = [];
    if (reduce) return;
    [].forEach.call(sl.querySelectorAll(".big"), function (el) {
      var n = el.firstChild;
      if (!n || n.nodeType !== 3) return;
      if (!el.dataset.t) el.dataset.t = n.nodeValue;
      var t = el.dataset.t, m = t.match(/^(\D*?)(\d[\d,]*(?:\.\d+)?)(\D*)$/);
      n.nodeValue = t;
      if (!m) return;
      var raw = m[2].replace(/,/g, ""), v = parseFloat(raw);
      if (v < 10 && raw.indexOf(".") < 0) return;
      var dec = (raw.split(".")[1] || "").length, comma = m[2].indexOf(",") >= 0, t0 = null;
      function tick(ts) {
        if (t0 === null) t0 = ts;
        var p = Math.min(1, (ts - t0) / 900), val = v * (1 - Math.pow(1 - p, 3));
        var s = val.toFixed(dec);
        if (comma) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        n.nodeValue = m[1] + s + m[3];
        if (p < 1) timers.push(requestAnimationFrame(tick));
      }
      timers.push(requestAnimationFrame(tick));
    });
  }

  function steps(i) { return parseInt(slides[i].dataset.steps || "0", 10); }

  function show(i, st) {
    cur = Math.max(0, Math.min(slides.length - 1, i));
    step = st === undefined ? 0 : st;
    slides.forEach(function (s, k) {
      var on = k === cur;
      if (!on && s.classList.contains("active")) s.classList.remove("active");
      if (!on) s.removeAttribute("data-step");
    });
    var sl = slides[cur];
    if (!sl.classList.contains("active")) {
      void sl.offsetWidth;
      sl.classList.add("active");
      countUp(sl);
    }
    if (steps(cur)) sl.setAttribute("data-step", step);
    num.textContent = cur + 1 + " / " + slides.length;
    ttl.textContent = sl.dataset.title || "";
    prog.style.width = ((cur + 1) / slides.length) * 100 + "%";
    try { history.replaceState(null, "", "#" + (cur + 1)); } catch (e) {}
  }

  function next() {
    if (step < steps(cur)) show(cur, step + 1);
    else if (cur < slides.length - 1) show(cur + 1, 0);
  }
  function prev() {
    if (step > 0) show(cur, step - 1);
    else if (cur > 0) show(cur - 1, steps(cur - 1));
  }

  function overview(on) {
    var b = document.body.classList;
    if (on === undefined) on = !b.contains("overview");
    b.toggle("overview", on);
    if (on) {
      slides.forEach(function (s) { s.classList.remove("active"); s.removeAttribute("data-step"); s.classList.remove("cur"); });
      slides[cur].classList.add("cur");
      stage.style.transform = "";
      slides[cur].scrollIntoView({ block: "center" });
    } else {
      resize();
      show(cur, step);
    }
  }

  function full() {
    if (document.fullscreenElement) document.exitFullscreen();
    else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
  }

  document.addEventListener("keydown", function (ev) {
    var k = ev.key;
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
    if (document.body.classList.contains("overview")) {
      if (k === "Escape" || k === "o" || k === "O") overview(false);
      return;
    }
    if (k === "ArrowRight" || k === "ArrowDown" || k === "PageDown" || k === " " || k === "Enter") { ev.preventDefault(); next(); }
    else if (k === "ArrowLeft" || k === "ArrowUp" || k === "PageUp" || k === "Backspace") { ev.preventDefault(); prev(); }
    else if (k === "Home") show(0);
    else if (k === "End") show(slides.length - 1);
    else if (k === "f" || k === "F") full();
    else if (k === "o" || k === "O") overview();
  });
  document.getElementById("bprev").onclick = prev;
  document.getElementById("bnext").onclick = next;
  document.getElementById("bover").onclick = function () { overview(); };
  document.getElementById("bfull").onclick = full;
  stage.addEventListener("click", function (ev) {
    if (!document.body.classList.contains("overview")) return;
    var s = ev.target.closest(".slide");
    if (!s) return;
    cur = slides.indexOf(s); step = 0;
    overview(false);
  });

  var x0 = null;
  vp.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  vp.addEventListener("touchend", function (e) {
    if (x0 === null) return;
    var d = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(d) > 50) { if (d < 0) next(); else prev(); }
  }, { passive: true });

  window.addEventListener("resize", resize);
  window.addEventListener("hashchange", function () {
    var h = location.hash.match(/^#(\d+)(?:\.(\d+))?/);
    if (h && h[1] - 1 !== cur) show(h[1] - 1, h[2] ? +h[2] : 0);
  });
  function start() {
    resize(); fit();
    var h = location.hash.match(/^#(\d+)(?:\.(\d+))?/);
    show(h ? h[1] - 1 : cur, h && h[2] ? +h[2] : 0);
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(start); else start();
})();
