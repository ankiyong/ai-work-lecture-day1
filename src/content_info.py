"""추가 장표: AI가 답변에 쓰는 정보는 어디서 오고, 언제 더 확인하는가. 강사 슬라이드 전용.
근거는 OpenAI 도움말 센터(2026.11.3 확인). 색: xk0 학습·일반 지식, xk1 첨부, xk2 웹, xk3 AI 제안, xk4 확인 안 됨."""
from lib import Sec, e, call, source
from motion import person, robot, DEFS

KICK = "AI 답변의 재료"
SEEN = " · 2026.11.3 확인"
H_DEV = "「How ChatGPT and our foundation models are developed」"
H_WEB = "「Searching the web with ChatGPT」"
H_TRUTH = "「Does ChatGPT tell the truth?」"
H_PROJ = "「Projects in ChatGPT」"

ICON = {
    "net": '<circle cx="9" cy="11" r="4"/><circle cx="9" cy="29" r="4"/><circle cx="31" cy="20" r="4"/><path d="M13 12l14 7M13 28l14-7M9 15v10"/>',
    "doc": '<path d="M10 5h14l7 7v23H10z"/><path d="M24 5v7h7M15 19h11M15 25h11M15 31h7"/>',
    "web": '<circle cx="20" cy="20" r="14"/><ellipse cx="20" cy="20" rx="6" ry="14"/><path d="M6 20h28M9 12h22M9 28h22"/>',
    "idea": '<path d="M20 4l3.5 12.5L36 20l-12.5 3.5L20 36l-3.5-12.5L4 20l12.5-3.5z"/>',
    "ask": '<circle cx="20" cy="20" r="14"/><path d="M15 16a5 5 0 1 1 7 4.6c-1.4.6-2 1.6-2 3V25M20 29.5v.5"/>',
}


def icon(name, k):
    return (f'<span class="xic {k}"><svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg></span>')


def mini(fn, **kw):
    return f'<svg class="xwho" viewBox="-46 -46 92 92" aria-hidden="true">{fn(0, 0, 44, cls="", **kw)}</svg>'


# ── 1. 세 곳 ───────────────────────────────────
def s_three():
    srcs = [("net", "xk0", "학습으로 익힌 지식·능력", "“보고서의 기본 구조를 설명해줘”"),
            ("doc", "xk1", "내가 준 정보 (대화·첨부)", "“첨부한 강의 계획서에서 교육 대상을 찾아줘”"),
            ("web", "xk2", "웹 검색으로 확인한 정보", "“올해 발표된 정책을 공식 자료에서 찾아줘”")]
    ins = "".join(f'<div class="xin {k}" style="--i:{i}">{icon(ic, k)}<div><h4>{e(t)}</h4><p>{e(q)}</p></div></div>'
                  for i, (ic, k, t, q) in enumerate(srcs))
    col = ["#26262a", "#0866d6", "#f26a10"]
    svg = ""
    for i, y in enumerate((64, 210, 356)):
        d = f"M0 {y}C90 {y} 80 210 138 210"
        svg += f'<path class="flowline xk{i}" d="{d}"/>'
        svg += f'<circle r="7" fill="{col[i]}"><animateMotion dur="1.8s" begin="-{i * .6:.1f}s" repeatCount="indefinite" path="{d}"/></circle>'
    out = "M262 210H392"
    svg += f'<path class="flowline" d="{out}" marker-end="url(#ah)"/>'
    for i, c in enumerate(col):
        svg += f'<circle r="7" fill="{c}"><animateMotion dur="1.8s" begin="-{i * .6:.1f}s" repeatCount="indefinite" path="{out}"/></circle>'
    svg += '<circle class="ring" cx="200" cy="210" r="58"/>' + robot(200, 210, 62, d=.5)
    mid = f'<svg class="xmid" viewBox="0 0 400 420" role="img" aria-label="세 가지 재료가 AI로 모여 하나의 답변이 되는 도식">{DEFS}{svg}</svg>'
    rows = [[("xk1", 34), ("xk0", 52)], [("xk0", 70)], [("xk2", 44), ("xk0", 40)], [("xk0", 30), ("xk1", 28), ("xk0", 22)], [("xk2", 60)], [("xk0", 46)]]
    n, lines = 0, ""
    for r in rows:
        seg = ""
        for k, w in r:
            seg += f'<i class="{k}" style="width:{w}%;--i:{n}"></i>'
            n += 1
        lines += f"<div>{seg}</div>"
    ans = (f'<div class="card xans"><h4>하나의 답변</h4><div class="xlines">{lines}</div>'
           '<p>세 가지는 따로 쓰이지 않고 한 답변 안에 섞입니다.</p>'
           '<p class="xnote">웹에서 가져온 내용을 이해하고 쉽게 풀어 쓰는 데도 학습한 능력이 쓰입니다.</p></div>')
    body = (f'<div class="xsrc"><div class="xins">{ins}</div>{mid}{ans}</div>'
            + source(f"근거: OpenAI 도움말 센터 {H_DEV}, 「Uploading files and audio to ChatGPT」, {H_WEB}{SEEN}"))
    return Sec(0, "답변의 재료는 세 곳에서 옵니다", KICK, body)


# ── 2. 찾아보지 않는다 ─────────────────────────
def s_not_lookup():
    shelf = "".join(f'<rect x="{292 + c * 44}" y="{24 + r * 64}" width="32" height="46" rx="4" class="xshelf"/>' for r in range(3) for c in range(4))
    left = (f'{robot(80, 115, 48, cls="xgray")}<path class="flowline xgrayl" d="M138 115H272"/>{shelf}'
            '<g class="xmag"><circle cx="300" cy="50" r="20"/><path d="M314 64l16 16"/></g>'
            '<g class="pop xstamp" style="--d:1.3"><circle cx="250" cy="115" r="86"/><path d="M190 55L310 175"/></g>')
    xs ={0: 50, 1: 160, 2: 270}
    right = ""
    for a in (0, 1):
        for y1 in [55, 115, 175] if a == 0 else [40, 95, 150, 205]:
            for y2 in ([40, 95, 150, 205] if a == 0 else [55, 115, 175]):
                right += f'<path class="xw" d="M{xs[a]} {y1}L{xs[a + 1]} {y2}"/>'
    for L, ys in ((0, [55, 115, 175]), (1, [40, 95, 150, 205]), (2, [55, 115, 175])):
        for j, y in enumerate(ys):
            right += f'<circle class="nd" style="--l:{L};--j:{j}" cx="{xs[L]}" cy="{y}" r="15"/>'
    right += '<path class="flowline" d="M300 115H420" marker-end="url(#ah)"/>' + robot(460, 115, 32, cls="pop", d=.2)
    toks = "".join(f'<span style="--i:{i}">{e(t)}</span>' for i, t in enumerate(["보고서는", "배경", "→ 문제", "→ 대안", "순서로", "씁니다"]))
    body = (
        '<div class="xvs">'
        f'<div class="xpane bad"><h5><span class="xmark">✗</span>답할 때마다 학습 자료 원본을 찾아본다</h5>'
        f'<svg class="xart" viewBox="0 0 500 230" aria-hidden="true">{DEFS}{left}</svg>'
        '<p>모델은 학습한 자료의 사본을 보관하지 않습니다. 꺼내 볼 책장이 없습니다.</p></div>'
        f'<div class="xpane good"><h5><span class="xmark">✓</span>익힌 패턴(가중치)으로 다음 말을 이어 만든다</h5>'
        f'<svg class="xart" viewBox="0 0 500 230" aria-hidden="true">{DEFS}{right}</svg>'
        f'<div class="xtok">{toks}</div></div>'
        '</div>'
        '<div class="xfix"><s>“학습한 데이터를 먼저 살펴본다”</s><span class="pulse">→</span><b>“학습으로 익힌 지식과 능력을 사용한다”</b></div>'
        + source(f"근거: OpenAI 도움말 센터 {H_DEV}: 모델은 학습 데이터 사본을 저장하지 않고, 학습된 가중치로 새 내용을 만든다{SEEN}"))
    return Sec(0, "학습 자료를 ‘찾아보는’ 것이 아닙니다", KICK, body)


# ── 3. 비율이 아니라 문장별 출처 ──────────────
def s_per_sentence():
    pie = ('<svg viewBox="0 0 220 220" aria-hidden="true"><g class="xpie">'
           '<circle cx="110" cy="110" r="72" fill="none" stroke="#26262a" stroke-width="32" pathLength="100" stroke-dasharray="80 100" transform="rotate(-90 110 110)"/>'
           '<circle cx="110" cy="110" r="72" fill="none" stroke="#f26a10" stroke-width="32" pathLength="100" stroke-dasharray="20 100" stroke-dashoffset="-80" transform="rotate(-90 110 110)"/>'
           '<text x="110" y="118" text-anchor="middle" font-size="26" font-weight="700" fill="#1d1d20">80 : 20</text></g>'
           '<path class="draw xstrike" pathLength="1" style="--d:1" d="M24 196L196 24"/></svg>')
    left = (f'<div class="xdon">{pie}<h4>“학습 80%, 검색 20%”</h4>'
            '<p>이렇게 나눌 수 없습니다. 웹 내용을 풀어 쓰는 데도 학습한 능력이 함께 쓰이기 때문입니다.</p></div>')
    sents = [("xk1", "교육 대상은 ○○부서 직원 40명입니다.", "첨부 · 계획서 1쪽"),
             ("xk2", "다른 기관의 최근 공고는 1일 6시간 과정이 많습니다.", "웹 · 출처 링크"),
             ("xk0", "실습형 교육은 보통 설명 → 시연 → 실습 순서로 짭니다.", "일반 지식 설명"),
             ("xk3", "2일차 끝에 부서별 사례 발표를 넣으면 좋겠습니다.", "AI 제안"),
             ("xk4", "강의실 정원은 계획서에서 확인되지 않습니다.", "확인 안 됨")]
    li = "".join(f'<li class="{k}" style="--i:{i}"><span>{e(t)}</span><em>{e(g)}</em></li>' for i, (k, t, g) in enumerate(sents))
    mock = (f'<div class="xmock"><div class="xq"><small>AI 답변 · 가상 예시</small><b>Q. 첨부한 강의 계획서로 교육 운영안을 정리해줘</b></div>'
            f'<ol class="xsent">{li}</ol></div>')
    body = f'<div class="xpct">{left}{mock}</div>' + call("볼 것은 비율이 아니라, 문장마다 ‘어디서 확인했는가’입니다")
    return Sec(0, "몇 %를 썼나보다, 무엇으로 확인했나", KICK, body)


# ── 4. 검색은 마지막 단계가 아니다 ────────────
def s_not_last():
    seq = "".join(f"<li>{e(x)}</li>" for x in ["학습한 지식으로 먼저 답해 본다", "막히면", "그때 검색한다"])
    rows = [("xk0", "net", "보고서 기획이 무엇인지 설명해줘", "일반 지식으로 설명할 수 있음", "개념을 묻는 질문"),
            ("xk2", "web", "오늘 발표된 정책을 알려줘", "처음부터 최신 자료를 확인", "학습 이후에 생긴 일"),
            ("xk2", "doc", "보고서 작성법을 정부 공식 지침에 근거해 설명해줘", "알고 있어도 원문·출처를 확인", "근거를 콕 집어 요구한 질문")]
    r = ""
    for i, (k, ic, q, h, p) in enumerate(rows):
        r += (f'<div class="xrow {k}" style="--i:{i}"><div class="xqb">{mini(person)}<span>“{e(q)}”</span></div>'
              '<svg class="xarr" viewBox="0 0 150 40" aria-hidden="true"><path class="flowline" d="M10 20H130"/><path d="M128 11l14 9-14 9z" style="fill:var(--k)"/></svg>'
              f'<div class="xr">{icon(ic, k)}<div><h4>{e(h)}</h4><p>{e(p)}</p></div></div></div>')
    body = (f'<div class="xseqw"><span class="xtag">흔한 오해</span><ol class="xseq">{seq}</ol><b class="xno">✗ 고정된 순서가 아님</b></div>'
            f'<div class="xroute"><h5 class="xrh">질문이 무엇을 요구하는지에 따라 처음부터 접근이 달라집니다</h5>{r}</div>'
            '<p class="xfoot">최신 정보가 도움이 되는 질문이면 AI가 스스로 검색하기도 하고, 사용자가 검색을 직접 켤 수도 있습니다.</p>'
            + source(f"근거: OpenAI 도움말 센터 {H_WEB}{SEEN}"))
    return Sec(0, "웹 검색은 ‘모를 때 마지막에’ 하는 것이 아닙니다", KICK, body)


# ── 5. 확신 ≠ 정확 ────────────────────────────
def s_confident():
    warns = "".join(f'<span style="--i:{i}">{e(w)}</span>' for i, w in enumerate(["틀린 날짜·수치", "없는 출처·인용", "복잡한 질문에 단정"]))
    checks = "".join(f'<li style="--i:{i}"><b>?</b>{e(c)}</li>' for i, c in enumerate(["언제 게시·수정된 자료인가", "원문이 이 문장을 정말 뒷받침하나", "공식 출처인가"]))
    body = (
        '<div class="xvs">'
        '<div class="xpane"><h5><span class="xmark">1</span>검색하지 않고 답했을 때</h5>'
        f'<div class="xbub">{mini(robot)}<div>○○제도는 2024년 3월부터 시행되었습니다.<small>근거 표시 없음</small></div></div>'
        f'<div class="xwarns">{warns}</div><div class="xbadge">확신하는 말투 ≠ 정확한 답</div></div>'
        '<div class="xpane"><h5><span class="xmark">2</span>검색해서 답했을 때</h5>'
        f'<div class="xbub">{mini(robot)}<div>○○제도는 2025년 1월부터 시행됩니다.<sup>1</sup></div></div>'
        '<div class="xsrcc"><div class="url"><sup>1</sup> 출처 열어 보기</div>'
        f'<ul>{checks}</ul><svg class="xglass" viewBox="0 0 40 40" aria-hidden="true"><circle cx="16" cy="16" r="11"/><path d="M24 24l11 11"/></svg></div>'
        '<div class="xbadge">검색 결과·인용도 틀리거나 오래될 수 있음</div></div>'
        '</div>'
        + call("어느 쪽이든, 중요한 사실은 원문을 열어 확인합니다")
        + source(f"근거: OpenAI 도움말 센터 {H_TRUTH}, {H_WEB}{SEEN}"))
    return Sec(0, "검색하지 않았다고 AI가 정확히 아는 것은 아닙니다", KICK, body)


# ── 6. 우선 ≠ 만 ──────────────────────────────
def s_only():
    doc = ('<div class="card xdoc">' + icon("doc", "xk1") + '<b>강의 계획서.pdf</b>'
           + "".join(f'<i style="width:{w}%"></i>' for w in (90, 70, 82)) + "</div>")
    bars = (f'<div class="xabr xk1" style="--i:0"><i style="width:58%"></i><span>계획서에서 확인</span></div>'
            f'<div class="xabr xk1" style="--i:1"><i style="width:42%"></i><span>계획서에서 확인</span></div>'
            f'<div class="xabr xk4" style="--i:2"><i style="width:50%"></i><span>첨부에 없는 설명</span></div>')
    ans = (f'<div class="card xab"><h4>AI 답변</h4>{bars}'
           '<div class="xwh"><span>학습한 일반 지식?</span><span>웹 검색?</span></div>'
           '<p class="xhint">겉모습만으로는 구분할 수 없습니다 → 출처를 표시해 달라고 요청</p></div>')
    vis = f'<div class="xfrow">{doc}<span class="pulse">→</span>{mini(robot)}<span class="pulse">→</span>{ans}</div>'
    myths = ('<div class="cards n3">'
             '<div class="card xmyth"><span class="xmark">✗</span><h4>“첨부자료만 쓴다”</h4><p>자료에 없는 일반 설명을 덧붙일 수 있습니다.</p></div>'
             '<div class="card xmyth"><span class="xmark">✗</span><h4>“없으면 자동으로 웹 검색한다”</h4><p>이런 처리 순서는 보장되지 않습니다.</p></div>'
             '<div class="card dark"><div class="tag">프로젝트에서는</div><ul><li>그 안의 대화·파일·지침을 맥락으로 씁니다</li><li>프로젝트 안에서도 웹 검색을 쓸 수 있습니다</li></ul></div>'
             '</div>')
    body = (vis + myths + call("쓸 자료의 범위와, 자료에 없을 때의 처리 방법은 직접 지시합니다")
            + source(f"근거: OpenAI 도움말 센터 {H_PROJ}, 「Uploading files and audio to ChatGPT」{SEEN}"))
    return Sec(0, "첨부자료를 ‘먼저’ 보는 것과 ‘만’ 쓰는 것은 다릅니다", KICK, body)


# ── 7. 자료에 없을 때 갈래 ────────────────────
def s_tree():
    leaves = [(1, "xk1", 10, "자료에 있음", "근거와 함께 답변 (파일명·쪽)", "예: 계획서에 정원이 적혀 있음"),
              (2, "xk0", 130, "내가 알려줄 정보가 없음", "‘확인 불가’라고 밝히고 나에게 질문", "예: 정원 미기재 → 다른 강의 정원으로 대신 ✗"),
              (3, "xk2", 250, "외부에서 확인할 사실", "웹 검색 + 첨부·웹 출처 구분", "예: 다른 기관 최신 강의 공고와 비교"),
              (4, "xk3", 370, "새로 만들어야 할 내용", "‘AI 제안’이라고 표시", "예: 계획서 개선 아이디어 → 원문과 구분")]
    h = ('<g class="pop" style="--d:0"><rect x="0" y="135" width="170" height="100" rx="14" fill="#26262a"/>'
         '<text x="85" y="180" text-anchor="middle" font-size="23" font-weight="700" fill="#fff">질문</text>'
         '<text x="85" y="208" text-anchor="middle" font-size="17" fill="#c9cad0">+ 첨부자료</text></g>'
         '<path class="draw br" pathLength="1" style="--d:.3" d="M172 185H216"/>'
         '<g class="pop" style="--d:.45"><path d="M330 112L446 185L330 258L214 185Z" fill="#fff" stroke="#26262a" stroke-width="2.5"/>'
         '<text x="330" y="180" text-anchor="middle" font-size="18" font-weight="600" fill="#1d1d20">자료에</text>'
         '<text x="330" y="204" text-anchor="middle" font-size="18" font-weight="600" fill="#1d1d20">답이 있나?</text></g>'
         '<path class="draw br l1" pathLength="1" style="--d:.8" d="M330 112V60H746"/>'
         '<text class="fade lbl l1" style="--d:1" x="344" y="92" font-size="17">있다</text>'
         '<path class="draw br l2 l3 l4" pathLength="1" style="--d:1.2" d="M330 258V300H508"/>'
         '<text class="fade lbl l2 l3 l4" style="--d:1.4" x="344" y="290" font-size="17">없다</text>'
         '<g class="pop br l2 l3 l4" style="--d:1.6"><rect x="510" y="258" width="190" height="84" rx="14" fill="#26262a"/>'
         '<text x="605" y="294" text-anchor="middle" font-size="19" font-weight="700" fill="#fff">무엇이</text>'
         '<text x="605" y="320" text-anchor="middle" font-size="19" font-weight="700" fill="#fff">부족한가?</text></g>')
    for n, path in ((2, "M700 300H722V180H746"), (3, "M700 300H746"), (4, "M700 300H722V420H746")):
        h += f'<path class="draw br l{n}" pathLength="1" style="--d:{1.8 + (n - 2) * .2:.1f}" d="{path}"/>'
    for n, k, y, c, a, x in leaves:
        d = 1.1 if n == 1 else 2 + (n - 2) * .25
        h += (f'<g class="lf l{n} {k}" style="--d:{d:.2f}"><rect class="lfb" x="750" y="{y}" width="426" height="100" rx="12"/>'
              f'<rect x="750" y="{y}" width="9" height="100" rx="4" style="fill:var(--k)"/>'
              f'<text class="c" x="776" y="{y + 28}">{e(c)}</text><text class="a" x="776" y="{y + 58}">{e(a)}</text>'
              f'<text class="x" x="776" y="{y + 86}">{e(x)}</text></g>')
    body = (f'<div class="xtree"><svg viewBox="0 0 1180 480" role="img" aria-label="첨부자료에 답이 없을 때 부족한 것에 따라 네 갈래로 처리하는 흐름">{h}</svg></div>'
            + call("자료에 없는 내용을 무조건 검색으로 채우지 않습니다"))
    return Sec(0, "자료에 없을 때는, 무엇이 부족한지부터 가릅니다", KICK, body, steps=4)


# ── 8. 지침으로 고정 ──────────────────────────
def s_rule():
    paras = [("① 근거 먼저", "첨부자료에서 먼저 관련 근거를 찾아 답변해줘. 파일명과 확인 가능한 페이지 또는 항목을 밝혀줘."),
             ("② 없을 때", "자료에서 확인되지 않는 사실은 임의로 채우지 말고, 확인되지 않았다고 표시해줘. 내가 알려줘야 하는 정보가 부족하면 나에게 질문해줘. 외부 자료로 확인해야 하는 내용은 웹 검색을 하고 출처를 밝혀줘."),
             ("③ 출처 구분", "답변에서는 첨부자료에서 확인한 사실, 웹에서 확인한 사실, 일반 지식에 따른 설명, AI의 추론·제안을 필요한 만큼 구분해줘.")]
    pr = "".join(f'<div class="xpp" style="--i:{i}"><b>{e(a)}</b><p>{e(b)}</p></div>' for i, (a, b) in enumerate(paras))
    leg = "".join(f'<li class="{k}" style="--i:{i}"><i></i>{e(t)}</li>' for i, (k, t) in enumerate(
        [("xk1", "첨부자료에서 확인"), ("xk2", "웹에서 확인 (출처)"), ("xk0", "일반 지식에 따른 설명"), ("xk3", "AI의 추론·제안"), ("xk4", "확인되지 않음")]))
    body = (
        '<div class="i-split wide">'
        f'<div class="xpr"><div class="xph">프로젝트 지침 예시 <small>복사해서 지침 칸에 붙여 넣기</small></div>{pr}</div>'
        '<div class="col">'
        f'<div class="card"><h4>답변에서 이렇게 구분됩니다</h4><ul class="xleg">{leg}</ul></div>'
        '<div class="card"><h4>어디에 넣나</h4><ul><li>ChatGPT 프로젝트 → 프로젝트 설정의 지침: 그 프로젝트 안에서만 적용</li>'
        '<li>Gemini Gem, Claude 프로젝트 → 지침 칸</li><li>일반 대화 → 첫 메시지에 붙여 넣기</li></ul></div>'
        '</div></div>'
        + source(f"근거: OpenAI 도움말 센터 {H_PROJ}: 프로젝트 지침은 그 프로젝트에만 적용되고 전역 맞춤 지침보다 우선{SEEN}"))
    return Sec(0, "원하는 처리 방식은 지침으로 정해 둡니다", KICK, body)


def add(d):
    """d: build.Deck"""
    chips = "".join(f'<span>{icon(ic, k)}{e(t)}</span>' for ic, k, t in
                    (("net", "xk0", "학습한 능력"), ("doc", "xk1", "내가 준 자료"), ("web", "xk2", "웹 검색")))
    d.dark('<p class="cover-tag anim">쉬어가기</p><h2 class="anim anim2">AI는 답의 재료를<br>어디서 가져올까?</h2>'
           f'<p class="subt anim anim2">그리고 언제 추가로 확인하는가</p><div class="xcov anim anim3">{chips}</div>', "AI는 답의 재료를 어디서 가져올까?", "sub")
    for s in (s_three(), s_not_lookup(), s_per_sentence(), s_not_last(), s_confident(), s_only(), s_tree(), s_rule()):
        d.content(s)
    d.dark('<p class="xold anim"><s>AI가 어떤 정보를 더 많이 썼나?</s></p>'
           '<h2 class="anim anim2">이번 답변의 사실은<br>어디에서 확인했나?</h2>'
           '<p class="subt anim anim3">그리고 확인하지 못한 내용은 무엇인가?</p>', "정리", "sub")


CSS = """
.xk0{--k:#26262a;--kt:#ececee}.xk1{--k:#0866d6;--kt:#e6f0fc}.xk2{--k:#f26a10;--kt:#fdeee3}.xk3{--k:#12a37a;--kt:#e2f5ef}.xk4{--k:#8a8b92;--kt:#f2f3f5}
.xic{width:52px;height:52px;border-radius:50%;background:var(--k);color:#fff;display:grid;place-items:center;flex:none}.xic svg{width:30px;height:30px}
.xwho{width:44px;height:44px;flex:none}
@keyframes xblink{50%{opacity:0}}
@keyframes xscan{0%,100%{transform:translate(0,0)}33%{transform:translate(132px,64px)}66%{transform:translate(44px,128px)}}
@keyframes xlit{0%,100%{fill:#d4d6dc}25%{fill:#0866d6}}
@keyframes xdim{to{opacity:.28}}
@keyframes xsweep{0%,100%{transform:translate(0,0)}50%{transform:translate(-150px,30px)}}
/* 세 곳 */
.xsrc{display:grid;grid-template-columns:380px 400px minmax(0,1fr);align-items:center}
.xins{display:flex;flex-direction:column;gap:18px}
.xin{height:128px;background:#fff;border:2px solid var(--k);border-radius:14px;padding:14px 16px;display:flex;gap:14px;align-items:center}
.xin h4{font-size:19.5px;color:var(--k);font-weight:700}.xin p{font-size:16px;color:var(--mid);margin-top:4px;line-height:1.4}
.xmid{width:400px;height:420px;display:block}.xmid .flowline{stroke:var(--k,#0866d6)}
.xans h4{font-size:21px!important}.xlines{display:grid;gap:13px;margin:16px 0}.xlines div{display:flex;gap:5px;height:15px}
.xlines i{display:block;height:100%;border-radius:8px;background:var(--k);transform-origin:left}
.slide .xans p{font-size:17px;color:var(--ink)}.slide .xans .xnote{font-size:15px;color:var(--mid);margin-top:10px;border-left:3px solid var(--sky);padding-left:10px}
.active .xin{animation:slidein .45s ease both;animation-delay:calc(var(--i)*.25s)}
.active .xans{animation:pop .5s ease both 1s}.active .xlines i{animation:growx .45s ease both;animation-delay:calc(1.3s + var(--i)*.1s)}
/* 찾아보지 않는다 */
.xvs{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:18px}
.xpane{background:#fff;border:2px solid var(--line);border-radius:14px;padding:16px 20px;display:flex;flex-direction:column;gap:10px}
.xpane.good{border-color:var(--blue)}.xpane h5{font-size:20px;font-weight:700;display:flex;gap:10px;align-items:center;line-height:1.35}
.xmark{width:30px;height:30px;border-radius:50%;display:grid;place-items:center;color:#fff;font-size:16px;flex:none;background:#6f7077;font-weight:700}.good .xmark{background:var(--blue)}
.xart{width:100%;height:auto;display:block}.slide .xpane p{font-size:17px;color:var(--mid)}
.xgray{filter:grayscale(1) brightness(1.35)}svg .xgrayl{stroke:#b5b7be}.xshelf{fill:#eceef1;stroke:#c6c8ce;stroke-width:2}
.xmag circle{fill:rgba(255,255,255,.4);stroke:#55565c;stroke-width:5}.xmag path{stroke:#55565c;stroke-width:7;stroke-linecap:round}
.active .xmag{animation:xscan 2.6s ease-in-out infinite}
.xstamp circle,.xstamp path{fill:none;stroke:#f26a10;stroke-width:9;stroke-linecap:round}
.xw{stroke:#dcdee3;stroke-width:1.5}.nd{fill:#d4d6dc}.active .nd{animation:xlit 1.8s ease-in-out infinite;animation-delay:calc(var(--l)*.3s + var(--j)*.05s)}
.xtok{display:flex;flex-wrap:wrap;gap:6px;align-items:center;min-height:42px}.xtok span{background:#e6f0fc;color:var(--blue);border-radius:8px;padding:5px 12px;font-size:19px;font-weight:600}
.xtok:after{content:"";width:3px;height:26px;background:var(--blue);animation:xblink 1s steps(1) infinite}
.active .xtok span{animation:pop .35s ease both;animation-delay:calc(.7s + var(--i)*.4s)}
.xfix{display:flex;align-items:center;gap:18px;justify-content:center;background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 20px;font-size:22px}
.xfix s{color:var(--soft);text-decoration:none;position:relative}.xfix s:after{content:"";position:absolute;left:-4px;right:-4px;top:52%;height:3px;background:var(--orange);transform-origin:left}
.active .xfix s:after{animation:growx .5s ease both 1.8s}.xfix b{color:var(--blue)}
/* 문장별 출처 */
.xpct{display:grid;grid-template-columns:320px minmax(0,1fr);gap:18px;align-items:stretch}
.xdon{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px;text-align:center;display:flex;flex-direction:column;justify-content:center;gap:8px}
.xdon svg{width:210px;height:210px;margin:0 auto;display:block}.xdon h4{font-size:21px}.slide .xdon p{font-size:16px;color:var(--mid);line-height:1.45}
svg .xstrike{stroke:#f26a10;stroke-width:7;stroke-linecap:round}.active .xpie{animation:xdim .5s ease both 1.5s}
.xmock{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 20px}
.xq{padding-bottom:10px;border-bottom:1px solid var(--line);margin-bottom:12px}.xq small{display:block;font-size:14px;color:var(--soft)}.xq b{font-size:19px;font-weight:600}
.xsent{display:grid;gap:10px}.xsent li{display:flex;justify-content:space-between;align-items:center;gap:14px;background:var(--kt);border-left:6px solid var(--k);border-radius:8px;padding:10px 14px;font-size:19px}
.xsent em{font-style:normal;font-size:15px;font-weight:600;color:#fff;background:var(--k);padding:4px 12px;border-radius:99px;white-space:nowrap;flex:none}
.xsent li.xk4{border-left-style:dashed;color:var(--mid)}
.active .xsent li{animation:slidein .4s ease both;animation-delay:calc(.25s + var(--i)*.3s)}.active .xsent em{animation:pop .4s ease both;animation-delay:calc(.5s + var(--i)*.3s)}
/* 마지막 단계 아님 */
.xseqw{display:flex;align-items:center;gap:22px;justify-content:center;background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 18px}
.xtag{background:#6f7077;color:#fff;border-radius:99px;padding:4px 12px;font-size:15px;flex:none}
.xseq{position:relative;display:flex;gap:38px}.xseq li{background:#f2f4f7;border-radius:9px;padding:8px 16px;font-size:19px;position:relative;color:var(--mid)}
.xseq li+li:before{content:"→";position:absolute;left:-28px;color:var(--soft)}
.xseq:after{content:"";position:absolute;left:-8px;right:-8px;top:50%;height:4px;background:var(--orange);transform-origin:left;border-radius:2px}
.active .xseq:after{animation:growx .6s ease both .6s}.xno{color:var(--orange);font-size:18px;flex:none}.active .xno{animation:pop .4s ease both 1.1s}
.xroute{display:grid;gap:12px}.xrh{font-size:18px;font-weight:600;color:var(--mid)}
.xrow{display:grid;grid-template-columns:minmax(0,1.1fr) 150px minmax(0,1fr);align-items:center}
.xqb{background:#fff;border:1px solid var(--line);border-radius:18px 18px 18px 4px;padding:12px 16px;font-size:19px;display:flex;gap:12px;align-items:center}
.xarr{width:150px;height:40px}.xarr .flowline{stroke:var(--k)}
.xr{background:var(--kt);border:2px solid var(--k);border-radius:14px;padding:12px 16px;display:flex;gap:14px;align-items:center}
.xr h4{font-size:19.5px;color:var(--k);font-weight:700}.slide .xr p{font-size:15.5px;color:var(--mid)}.xr .xic{width:44px;height:44px}.xr .xic svg{width:26px;height:26px}
.active .xrow .xqb{animation:slidein .4s ease both;animation-delay:calc(1.3s + var(--i)*.5s)}.active .xrow .xarr{animation:fadein .3s ease both;animation-delay:calc(1.5s + var(--i)*.5s)}
.active .xrow .xr{animation:pop .45s ease both;animation-delay:calc(1.6s + var(--i)*.5s)}
.xfoot{font-size:16px;color:var(--mid);text-align:center}
/* 확신 */
.xbub{display:flex;gap:12px;align-items:flex-start}.xbub>div{background:#f2f4f7;border-radius:4px 16px 16px 16px;padding:12px 16px;font-size:20px;font-weight:600}
.xbub small{display:block;font-size:14px;font-weight:400;color:var(--soft);margin-top:2px}
.xbub sup,.xsrcc sup{background:var(--blue);color:#fff;border-radius:6px;padding:1px 6px;font-size:13px;margin-left:4px;vertical-align:4px}
.xwarns{display:flex;gap:8px;flex-wrap:wrap}.xwarns span{background:#fdeee3;color:#b44a05;border-radius:99px;padding:6px 14px;font-size:16px;font-weight:600}
.xbadge{margin-top:auto;background:var(--dark);color:#fff;border-radius:10px;padding:10px 14px;font-size:18px;font-weight:600;text-align:center}
.xsrcc{border:2px dashed #c6c8ce;border-radius:10px;padding:10px 16px;position:relative;overflow:hidden}.xsrcc .url{font-size:15px;color:var(--mid);margin-bottom:6px}
.xsrcc ul{display:grid;gap:6px}.xsrcc li{font-size:17px;display:flex;gap:10px;align-items:center}
.xsrcc li b{width:24px;height:24px;border-radius:50%;background:var(--orange);color:#fff;display:grid;place-items:center;font-size:14px;flex:none}
.xglass{position:absolute;right:20px;top:14px;width:46px;height:46px}.xglass circle{fill:rgba(47,150,247,.12);stroke:var(--blue);stroke-width:3.5}.xglass path{stroke:var(--blue);stroke-width:5;stroke-linecap:round}
.active .xglass{animation:xsweep 3s ease-in-out infinite 1s}
.active .xbub{animation:rise .45s ease both .2s}.active .xwarns span{animation:pop .4s ease both;animation-delay:calc(.8s + var(--i)*.25s)}
.active .xsrcc li{animation:slidein .4s ease both;animation-delay:calc(.8s + var(--i)*.25s)}.active .xbadge{animation:rise .45s ease both 1.7s}
/* 우선 ≠ 만 */
.xfrow{display:grid;grid-template-columns:200px 40px 70px 40px minmax(0,1fr);align-items:center;gap:8px}.xfrow .xwho{width:70px;height:70px}
.xdoc{display:flex;flex-direction:column;gap:8px;align-items:flex-start}.xdoc b{font-size:16px}.xdoc>i{display:block;height:9px;border-radius:5px;background:#c9dcf5}
.xab{display:grid;gap:8px}.xab h4{font-size:19px!important}
.xabr{display:grid;grid-template-columns:minmax(0,1fr) 160px;gap:12px;align-items:center}.xabr i{display:block;height:16px;border-radius:8px;background:var(--k);transform-origin:left}
.xabr span{font-size:15.5px;color:var(--k);font-weight:600}.xabr.xk4 i{background:repeating-linear-gradient(90deg,#b5b7be 0 12px,transparent 12px 18px)}
.xwh{display:flex;gap:10px}.xwh span{border:2px dashed #b5b7be;border-radius:99px;padding:4px 14px;font-size:16px;color:var(--mid)}
.slide .xhint{font-size:16.5px;color:var(--blue);font-weight:600}
.xmyth{position:relative}.xmyth .xmark{background:var(--orange);position:absolute;top:16px;right:16px}
.xmyth h4{display:inline-block;position:relative;color:var(--mid)}.xmyth h4:after{content:"";position:absolute;left:-3px;right:-3px;top:54%;height:3px;background:var(--orange);transform-origin:left}
.active .xmyth h4:after{animation:growx .5s ease both 1.6s}
.active .xfrow>*{animation:rise .45s ease both}.active .xfrow>:nth-child(3){animation:pop .45s ease both .3s}.active .xfrow>:nth-child(5){animation-delay:.5s}
.active .xabr i{animation:growx .5s ease both;animation-delay:calc(.8s + var(--i)*.25s)}.active .xwh span{animation:pop .4s ease both 1.6s}.active .xwh span+span{animation-delay:1.8s}
/* 갈래 */
.xtree svg{width:100%;height:auto;display:block}.xtree text{font-family:inherit}
.xtree .draw.br{stroke:#9ea1aa}.xtree .lbl{fill:var(--mid);font-weight:600}
.xtree .lfb{fill:#fff;stroke:var(--k);stroke-width:2.5}.xtree .lf .c{fill:var(--k);font-size:15px;font-weight:600}.xtree .lf .a{font-size:21px;font-weight:700;fill:#1d1d20}.xtree .lf .x{font-size:15.5px;fill:#55565c}
.xtree .lf,.xtree .br,.xtree .lbl{transition:opacity .3s}.active .xtree .lf{animation:slidein .45s ease both;animation-delay:calc(var(--d)*1s)}
.slide[data-step="1"] .xtree :is(.lf,.br,.lbl):not(.l1),.slide[data-step="2"] .xtree :is(.lf,.br,.lbl):not(.l2),
.slide[data-step="3"] .xtree :is(.lf,.br,.lbl):not(.l3),.slide[data-step="4"] .xtree :is(.lf,.br,.lbl):not(.l4){opacity:.15}
.slide[data-step="1"] .xtree .l1 .lfb,.slide[data-step="2"] .xtree .l2 .lfb,.slide[data-step="3"] .xtree .l3 .lfb,.slide[data-step="4"] .xtree .l4 .lfb{fill:var(--kt)}
.slide[data-step="1"] .xtree path.l1,.slide[data-step="2"] .xtree path.l2,.slide[data-step="3"] .xtree path.l3,.slide[data-step="4"] .xtree path.l4{stroke:#0866d6}
/* 지침 */
.xpr{background:var(--dark);color:#fff;border-radius:14px;padding:16px 22px;display:grid;gap:12px}
.xph{font-size:16px;color:var(--sky);font-weight:600}.xph small{color:#a9abb3;font-weight:400;margin-left:8px;font-size:14px}
.xpp{display:grid;grid-template-columns:116px minmax(0,1fr);gap:14px;align-items:start;border-top:1px solid #3a3a40;padding-top:12px}
.xpp b{background:var(--sky);color:#06233f;border-radius:8px;padding:6px 8px;font-size:15px;text-align:center}
.slide .xpp p{font-size:18.5px;line-height:1.65;color:#f1f1f3}
.active .xpp{animation:rise .45s ease both;animation-delay:calc(.2s + var(--i)*.35s)}
.xleg{display:grid;gap:9px;margin-top:10px}.slide .xleg li{display:flex;gap:10px;align-items:center;font-size:17px;color:var(--ink)}
.xleg i{width:18px;height:18px;border-radius:5px;background:var(--k);flex:none}.xleg .xk4 i{background:none;border:2px dashed var(--k)}
.active .xleg li{animation:slidein .35s ease both;animation-delay:calc(1.2s + var(--i)*.15s)}
/* 표지·정리 */
.xcov{display:flex;gap:34px;margin-top:50px}.xcov span{display:flex;align-items:center;gap:12px;font-size:23px}.dark-slide .xk0{--k:#55565c}
.xold{font-size:28px;color:#8a8b92}.xold s{text-decoration-color:var(--orange);text-decoration-thickness:3px}
"""
