"""python src/build.py → docs/index.html(수강생), docs/instructor/index.html(강사 슬라이드쇼) 생성.
개정안(보고서 흐름: 기획 3단계 → 작성 5단계 → 최종 검토)은 docs/v2/에 따로 만든다."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import config as C
import content_a as A
import content_b as B
import content_c as X
import content_v2 as V
import content_info as I
import content_v3 as W
import lib
from lib import e

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = (ROOT / "src/style.css").read_text(encoding="utf-8")
JS = (ROOT / "src/app.js").read_text(encoding="utf-8")
DECK_CSS = (ROOT / "src/slides.css").read_text(encoding="utf-8")
DECK_JS = (ROOT / "src/slides.js").read_text(encoding="utf-8")
FONT = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">'
ROBOTS = '<meta name="robots" content="noindex,nofollow">'

BREAKS = {"06": "다음 모듈: GPT와 정책보고서 기획하기", "07": "다음 모듈: 보고서 작성 방법 이해하기", "09": "다음 모듈: Gemini Notebook 이해하기"}


def modules():
    return [A.m01(), A.m02(), X.m03(), A.m04(), X.m05(), X.m06(), B.m07(), X.m08(), B.m09(), B.m10()]


class Ver:
    """dir: docs 아래 폴더, store: 입력 저장 이름, label: 제목 뒤 표시, extra: 모듈 번호 → 그 모듈 뒤에 장을 더하는 함수(강사 슬라이드만),
    js: 수강생 페이지에 덧붙이는 스크립트."""
    def __init__(self, dir, intro, mods, breaks, store="eid-d1:", label="", steps=None, css="", deck_css="", extra=None, js=""):
        self.dir, self.intro, self.mods, self.breaks = dir, intro, mods, breaks
        self.store, self.label, self.steps, self.css, self.deck_css = store, label, steps, css, deck_css
        self.extra, self.js = {} if extra is None else extra, js


V1 = Ver("", A.intro_secs, modules, BREAKS)
V2 = Ver("v2", V.intro_secs, V.modules, V.BREAKS, "eid-d1v2:", " · 개정안", V.STEPS, V.CSS, V.DECK_CSS + I.CSS, {"05": I.add})
V3 = Ver("v3", W.intro_secs, W.modules, W.BREAKS, "eid-d1v3:", " · 실습 개정안", W.STEPS, W.CSS, W.DECK_CSS, W.EXTRA, W.JS)


# ── 수강생 페이지 ──────────────────────────────
def student_sec(s, sid):
    if s.role == "i":
        return "", None
    top = f'<div class="kick"><span>{e(s.kicker)}</span>'
    if s.step:
        top += lib.stepmap(*s.step)
    top += "</div>"
    return f'<section class="sec" id="{sid}"><header>{top}<h3>{e(s.title)}</h3></header>{s.body}</section>', (sid, s.title)


def student_page(v=V1):
    lib.set_role("student")
    lib.set_steps(v.steps)
    body, nav = "", ""
    intro = ('<section class="sec" id="howto"><header><div class="kick"><span>시작 전에</span></div><h3>이 페이지 사용법</h3></header>'
             + lib.cards(lib.card("입력은 이 브라우저에만 저장", "자동 저장되며 서버로 보내지 않습니다", "공용 PC라면 마친 뒤 입력 지우기를 누르세요"),
                         lib.card("복사해서 이어 가기", "표마다 있는 마크다운 복사로 다음 단계 프롬프트에 붙여 넣습니다", "예시 프롬프트는 내 것을 쓴 뒤에 열어 봅니다"),
                         lib.card("민감정보 입력 금지", "내부 정보와 개인정보는 이 페이지와 외부 AI에 입력하지 않습니다"))
             + "</section>")
    for n, s in enumerate(v.intro()):
        intro += student_sec(s, f"intro-{n}")[0]
    body += f'<div class="mod" id="start">{intro}</div>'
    nav += '<a href="#start" class="nm"><b>0</b>시작하기</a>'
    for m in v.mods():
        rendered, sub = "", ""
        for k, s in enumerate(m.secs):
            h, item = student_sec(s, f"m{m.num}-{k}")
            rendered += h
            if item:
                sub += f'<a href="#{item[0]}">{e(item[1])}</a>'
        if not rendered:
            continue
        meta = f"<span>결과물: {e(m.result)}</span>"
        if m.tool:
            meta += f"<span>도구: {e(m.tool)}</span>"
        body += f'<div class="mod" id="m{m.num}"><div class="hero"><b>{m.num}</b><h2>{e(m.title)}</h2><p>{e(m.intro)}</p><div class="meta">{meta}</div></div>{rendered}</div>'
        nav += f'<details class="ng"><summary><a href="#m{m.num}" class="nm"><b>{m.num}</b>{e(m.title)}</a></summary><div>{sub}</div></details>'
    js = JS.replace('"eid-d1:"', f'"{v.store}"') + v.js
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI와 함께하는 업무 · 실습 안내{v.label}</title>{ROBOTS}{FONT}
<style>{CSS}{v.css}</style></head>
<body class="student">
<header class="top"><button type="button" class="btn menu" id="menu" aria-expanded="false" aria-controls="nav">목차</button>
<div class="brand"><small>기획예산처 AI 활용 특강 · 1일차 · EID Consulting{v.label}</small><strong>AI와 함께하는 업무</strong></div>
<span class="role">실습 안내</span><div class="tools"><button type="button" class="btn" id="exportMd">내 결과 내려받기</button><button type="button" class="btn" id="clearAll">입력 지우기</button></div></header>
<div class="layout"><nav id="nav" aria-label="목차">{nav}</nav>
<main><div class="cover"><p>문제 찾기부터 정책보고서·인포그래픽까지</p><div><span>조사</span><span>기획</span><span>작성</span><span>시각화</span></div></div>{body}</main></div>
<div id="toast" role="status" aria-live="polite"></div>
<script>{js}</script></body></html>
"""


# ── 강사 슬라이드쇼 ────────────────────────────
class Deck:
    def __init__(self):
        self.items = []

    def dark(self, html, title, cls=""):
        self.items.append((f"dark-slide {cls}", title, 0, html))

    def content(self, s):
        step = lib.stepmap(*s.step) if s.step else ""
        html = (f'<header class="sh"><div class="kick"><span>{e(s.kicker)}</span></div>{step}<h3>{e(s.title)}</h3></header>'
                f'<div class="body">{s.body}</div>')
        self.items.append(("", s.title, s.steps, html))

    def render(self):
        out, n = "", len(self.items)
        for i, (cls, title, steps, html) in enumerate(self.items, 1):
            attr = f' data-steps="{steps}"' if steps else ""
            out += (f'<section class="slide {cls}" data-title="{e(title)}"{attr}>'
                    f'<img class="logo" src="../assets/logo.png" alt="EID Consulting">{html}<span class="pgno">{i}</span></section>')
        return out, n


def add_sec(d, s):
    if s.kind == "image":
        d.items.append(("image-slide", s.title, 0, f'<div class="imgonly"><img src="../assets/{s.kicker}" alt="{e(s.body)}"></div>'))
    elif s.kind == "raw":  # 머리글 없이 본문을 그대로 쓰는 장. kicker 자리에 장 클래스
        d.items.append((s.kicker, s.title, s.steps, s.body))
    elif s.kind == "sub":
        d.dark(f'<h2 class="anim">{e(s.title)}</h2><p class="subt anim anim2">{e(s.kicker)}</p>', s.title, "sub")
    else:
        d.content(s)


def deck_page(v=V1):
    lib.set_role("instructor")
    lib.set_steps(v.steps)
    d = Deck()
    d.dark(f'<div class="cv"><p class="cover-tag anim">기획예산처 AI 활용 특강{v.label}</p><p class="main anim anim2">AI와 함께하는 업무</p>'
           '<p class="subt anim anim2">문제 찾기부터 정책보고서·인포그래픽까지</p><div class="row anim anim3"><span><i></i>조사</span><span><i></i>기획</span><span><i></i>작성</span><span><i></i>시각화</span></div></div>', "AI와 함께하는 업무")
    for s in v.intro():
        add_sec(d, s)
    for m in v.mods():
        if m.num in v.breaks:
            d.dark(f'<div class="cup anim" aria-hidden="true">☕</div><h2 class="anim anim2">휴식</h2><p class="subt anim anim3">{e(v.breaks[m.num])}</p>', "휴식", "sub")
        d.dark(f'<div class="num anim">{m.num}</div><h2 class="anim anim2">{e(m.title)}</h2><p class="subt anim anim3">결과물: {e(m.result)}</p>', f"{m.num} {m.title}")
        for s in m.secs:
            add_sec(d, s)
        if m.num in v.extra:
            v.extra[m.num](d)
    slides, n = d.render()
    base = "\n".join(l for l in (CSS + v.css).splitlines() if not l.startswith("@media"))
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI와 함께하는 업무 · 강의 슬라이드{v.label}</title>{ROBOTS}{FONT}
<style>{base}
{DECK_CSS}{v.deck_css}</style></head>
<body class="deckbody">
<div id="viewport"><div id="stage">{slides}</div></div>
<div id="bar"><button type="button" id="bprev" aria-label="이전">◀ 이전</button><button type="button" id="bnext" aria-label="다음">다음 ▶</button>
<span class="count" id="count" aria-live="polite">1 / {n}</span><div id="prog"><i id="progi"></i></div><span class="ttl" id="ttl"></span>
<button type="button" id="bover" title="O 키">전체 보기</button><button type="button" id="bfull" title="F 키">전체 화면</button></div>
<script>{DECK_JS}</script></body></html>
"""


def main():
    out = ROOT / "docs"
    for v in (V1, V2, V3):
        d = out / v.dir if v.dir else out
        (d / "instructor").mkdir(parents=True, exist_ok=True)
        s, i = student_page(v), deck_page(v)
        if v.dir:  # 한 단계 아래 폴더: 공용 assets 경로를 맞춘다
            s = s.replace('="assets/', '="../assets/')
            i = i.replace('="../assets/', '="../../assets/')
        (d / "index.html").write_text(s, encoding="utf-8")
        (d / "instructor/index.html").write_text(i, encoding="utf-8")
    lib.set_steps(None)
    (out / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    print("built", out)


if __name__ == "__main__":
    main()
