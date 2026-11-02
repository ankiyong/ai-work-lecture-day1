(function () {
  var PREFIX = "eid-d1:" + (document.body.className.indexOf("instructor") >= 0 ? "i:" : "s:");
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var toastTimer;
  function toast(t) {
    var el = document.getElementById("toast");
    el.textContent = t; el.classList.add("on");
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { el.classList.remove("on"); }, 1800);
  }
  function save(k, v) { try { if (v === "" || v === false) localStorage.removeItem(PREFIX + k); else localStorage.setItem(PREFIX + k, String(v)); } catch (e) {} }
  function load(k) { try { return localStorage.getItem(PREFIX + k); } catch (e) { return null; } }

  $$("[data-k]").forEach(function (el) {
    var k = el.getAttribute("data-k"), v = load(k);
    if (el.type === "checkbox") {
      el.checked = v === "true";
      el.addEventListener("change", function () { save(k, el.checked); });
    } else {
      if (v !== null) el.value = v;
      el.addEventListener("input", function () { save(k, el.value); });
    }
  });

  function copy(text, msg) {
    function done() { toast(msg || "복사했습니다"); }
    function fallback() {
      var t = document.createElement("textarea");
      t.value = text; document.body.appendChild(t); t.select();
      try { document.execCommand("copy"); done(); } catch (e) { toast("복사하지 못했습니다"); }
      t.remove();
    }
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, fallback);
    else fallback();
  }

  function cell(s) { return String(s).replace(/\|/g, "\\|").replace(/\n/g, " ").trim(); }
  function formMd(f) {
    var kind = f.getAttribute("data-kind");
    if (kind === "prompt") return f.querySelector("textarea").value;
    var title = "## " + f.getAttribute("data-title") + "\n";
    if (kind === "fields") {
      return title + $$(".field", f).map(function (l) {
        return "- **" + l.querySelector("span").textContent + "**: " + cell(l.querySelector("textarea").value);
      }).join("\n");
    }
    var head = $$("thead th", f).map(function (h) { return h.textContent; });
    var rows = $$("tbody tr", f).map(function (r) {
      return "| " + cell(r.querySelector("th").textContent) + " | " + $$("textarea", r).map(function (t) { return cell(t.value); }).join(" | ") + " |";
    });
    return title + "| " + head.join(" | ") + " |\n|" + head.map(function () { return "---"; }).join("|") + "|\n" + rows.join("\n");
  }

  /* 앞 단계 결과: 비어 있으면 건너뛰고, 표는 채운 행만 넘긴다 */
  function srcMd(id) {
    var f = document.querySelector('.form[data-src="' + id + '"]');
    if (!f || !$$("textarea", f).some(function (t) { return t.value.trim(); })) return "";
    var md = formMd(f);
    if (f.getAttribute("data-kind") === "table") {
      md = md.split("\n").filter(function (ln, i) {
        return i < 3 || ln.split("|").slice(2, -1).some(function (c) { return c.trim(); });
      }).join("\n");
    } else {
      md = md.split("\n").filter(function (ln) { return !/\*\*: *$/.test(ln); }).join("\n");
    }
    return md;
  }
  function slotText(sv) {
    var s = "";
    (function walk(n) {
      [].forEach.call(n.childNodes, function (c) {
        if (c.nodeType === 3) s += c.nodeValue;
        else if (c.tagName === "BR") s += "\n";
        else if (c.tagName === "INPUT" || c.tagName === "TEXTAREA") s += c.value.trim() || "[" + (c.getAttribute("data-blank") || c.getAttribute("aria-label") || "입력") + "]";
        else if (c.tagName !== "BUTTON") walk(c);
      });
    })(sv);
    return s.trim();
  }
  function assemble(b) {
    if (b.getAttribute("data-level") === "3") return b.querySelector("[data-free]").value;
    return $$(".slot", b).map(function (sl) {
      var t = slotText(sl.querySelector(".sv")), etc = sl.querySelector("[data-etc]");
      if (etc && etc.value.trim()) t += "\n" + etc.value.trim();
      return "[" + sl.getAttribute("data-slot") + "]  " + t;
    }).join("\n");
  }
  function refresh() {
    $$("[data-from]").forEach(function (t) {
      if (load(t.getAttribute("data-k") + ":dirty") !== "true") t.value = srcMd(t.getAttribute("data-from"));
    });
    $$(".builder").forEach(function (b) {
      var o = b.querySelector("[data-out]");
      if (o) o.textContent = assemble(b);
    });
  }
  document.addEventListener("input", function (ev) {
    var t = ev.target;
    if (t.hasAttribute && t.hasAttribute("data-from")) save(t.getAttribute("data-k") + ":dirty", "true");
    refresh();
  });
  refresh();

  document.addEventListener("click", function (ev) {
    var b = ev.target.closest && ev.target.closest("button");
    if (!b) return;
    if (b.hasAttribute("data-bcopy")) {
      var txt = assemble(b.closest(".builder"));
      if (txt.trim()) copy(txt, "프롬프트를 복사했습니다"); else toast("아직 입력한 내용이 없습니다");
    }
    if (b.hasAttribute("data-srccopy")) {
      var md0 = srcMd(b.getAttribute("data-srccopy"));
      if (md0) copy(md0, "이전 결과를 복사했습니다"); else toast("해당 표가 아직 비어 있습니다");
    }
    if (b.hasAttribute("data-refill")) {
      var ta = b.parentNode.querySelector("[data-from]");
      save(ta.getAttribute("data-k") + ":dirty", "");
      refresh();
      toast(ta.value ? "이전 결과를 가져왔습니다" : "해당 표가 아직 비어 있습니다");
    }
    if (b.hasAttribute("data-copy")) copy(b.closest(".prompt").querySelector("pre").textContent);
    if (b.hasAttribute("data-mdcopy")) {
      var f = b.closest(".form");
      copy(formMd(f), f.getAttribute("data-kind") === "prompt" ? "프롬프트를 복사했습니다" : "마크다운으로 복사했습니다");
    }
  });

  var exp = document.getElementById("exportMd");
  if (exp) exp.addEventListener("click", function () {
    var parts = $$(".form").filter(function (f) {
      return f.getAttribute("data-kind") !== "prompt" && $$("textarea", f).some(function (t) { return t.value.trim(); });
    }).map(formMd);
    if (!parts.length) { toast("아직 입력한 내용이 없습니다"); return; }
    var url = URL.createObjectURL(new Blob(["# AI와 함께하는 업무: 내 결과물\n\n" + parts.join("\n\n") + "\n"], { type: "text/markdown;charset=utf-8" }));
    var a = document.createElement("a");
    a.href = url; a.download = "내_결과물.md"; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  });

  var clr = document.getElementById("clearAll");
  if (clr) clr.addEventListener("click", function () {
    if (!confirm("이 브라우저에 저장된 입력을 모두 지울까요? 되돌릴 수 없습니다.")) return;
    $$("[data-k]").forEach(function (el) {
      if (el.type === "checkbox") el.checked = false; else el.value = el.defaultValue || "";
      save(el.getAttribute("data-k"), "");
      save(el.getAttribute("data-k") + ":dirty", "");
    });
    refresh();
    toast("입력을 지웠습니다");
  });

  var tn = document.getElementById("toggleNotes");
  if (tn) tn.addEventListener("click", function () {
    var off = document.body.classList.toggle("hide-notes");
    tn.textContent = off ? "노트 보이기" : "노트 숨기기";
  });

  var nav = document.getElementById("nav"), menu = document.getElementById("menu");
  menu.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    menu.setAttribute("aria-expanded", open);
  });
  nav.addEventListener("click", function (ev) {
    var a = ev.target.closest("a");
    if (!a) return;
    nav.classList.remove("open"); menu.setAttribute("aria-expanded", "false");
    var g = a.closest(".ng"); if (g) g.open = true;
  });

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (x) {
        if (!x.isIntersecting) return;
        $$("nav a.cur").forEach(function (a) { a.classList.remove("cur"); });
        var a = nav.querySelector('a[href="#' + x.target.id + '"]');
        if (a) { a.classList.add("cur"); var g = a.closest(".ng"); if (g) g.open = true; }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    $$(".sec[id]").forEach(function (s) { io.observe(s); });
  }
})();
