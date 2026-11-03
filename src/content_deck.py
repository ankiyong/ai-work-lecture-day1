"""v3 추가분: 강사소개 장(표지 다음), '보고서를 HTML 발표장표로 바꾸기' 모듈.
모듈은 강사의 ChatGPT 대화 사례(2022년 기획재정부 주요업무 추진계획 → 20장 HTML 장표)를 3단계 프롬프트로 정리한 것이다."""
from lib import Mod, Sec, call, card, cards, check, e, flow, is_i, only_s, source
from motion import chevrons
import content_p as P

K = "보고서 → HTML 발표장표"
CASE = "사례: 강사의 ChatGPT 대화 — 「2022년 기획재정부 주요업무 추진계획」(2021.12.22.)으로 20장 HTML 장표 제작"


# ── 강사소개 (PDF의 장면 순서: 해시태그 → 사진 셋과 이름 → 경력) ─────
def intro_slide():
    tags = "".join(f'<span style="--i:{i}">{t}</span>' for i, t in enumerate(("#유쾌", "#공감", "#핸섬")))
    career = ["(전) 데이터 엔지니어", "(전) DevOps", "(현) 생성형AI 전문 강사", "(현) 대학생 진로 강사",
              "(현) 팀빌딩 &amp; 레크레이션 강사", "(현) 여친 없음", "(전) 여친 다수"]
    li = "".join(f'<li style="--i:{i}">{c}</li>' for i, c in enumerate(career))
    img = lambda c, alt: f'<img class="ti-p ti-{c}" src="../assets/instructor/ahn-{c}.png" alt="{alt}">'
    body = (f'<div class="ti"><h2 class="ti-h">강사소개</h2><div class="ti-tags">{tags}</div>'
            + img("left", "") + img("center", "안기용 강사") + img("right", "")
            + f'<p class="ti-name">안기용<b>강사</b></p><ul class="ti-list">{li}</ul></div>')
    return Sec(0, "강사소개", "intro-slide", body, role="i", steps=2, kind="raw")


# ── 보고서 → HTML 발표장표 ─────────────────────
PROMPTS = {
    "A": ("핵심 내용 정리", "첨부한 보고서를 바탕으로 발표 장표를 만들 것이다.\n"
          "우선 내용을 파악해서 발표에 들어가야 할 핵심 내용을 정리해줘.\n발표 장표 수는 제한 없다."),
    "B": ("장표별 내용 확정", "아래 조건으로 발표자료 구성을 확정한다.\n\n"
          "[발표 스타일]\n[[#발표 스타일|정책보고형 / 강의·교육형 / 핵심요약형 중 선택]]\n\n"
          "[발표 대상]\n[[#발표 대상|여기에 입력|예: 공무원·공공기관 관계자]]\n\n"
          "[발표 시간]\n[[#발표 시간|여기에 입력|예: 20~30분]]\n\n"
          "장표별로 포함될 내용을 구체적으로 정리해줘.\n보고서에 없는 효과나 성과는 확정된 사실처럼 쓰지 마."),
    "C": ("HTML 장표 만들기", "첨부한 디자인을 참고해서 HTML 장표로 만들어줘.\n\n"
          "[디자인 참고 자료]\n[[#디자인 참고 자료|첨부한 파일 이름|예: 디자인 가이드.pdf]]\n\n"
          "각 장표에 이미지·도식을 활용해서 이해를 돕도록 해야 함.\n모션그래픽을 활용해서 생동감 있는 장표로 구성해줘.\n"
          "앞에서 확정한 장표별 내용과 수치를 그대로 사용해줘."),
}


def pblock(k):
    name, text = PROMPTS[k]
    if is_i():
        return f'<div class="prompt"><div class="ph"><span>프롬프트 {k} · {e(name)}</span></div><pre>{P.tpl("h" + k, text)}</pre></div>'
    return (f'<div class="tpl"><div class="ph"><span>프롬프트 {k} · {e(name)} · 빈칸을 채운 뒤 복사</span>'
            f'<button type="button" class="btn pri" data-tcopy>복사</button></div><div class="tv">{P.tpl("h" + k, text)}</div></div>')


def options():
    groups = [("발표 스타일", ["정책보고형", "강의·교육형", "핵심요약형"]), ("발표 대상", ["공무원·공공기관 관계자", "대학생·일반인", "간부·의사결정자"]),
              ("발표 시간", ["10~15분", "20~30분", "40~60분"])]
    h, n = "", 0
    for g, opts in groups:
        o = ""
        for x in opts:
            o += f'<span style="--i:{n}">{e(x)}</span>'
            n += 1
        h += f'<div class="dopt"><b>{e(g)}</b><div>{o}</div></div>'
    return f'<div class="card dopts"><h4>AI가 준 선택지 — 고르는 것은 나</h4>{h}</div>'


def plan_bar():
    segs = [("도입", 2), ("성과·여건", 3), ("① 경제정상화", 3), ("② 혁신성장", 4), ("③ 포용성장", 3), ("④ 리스크", 2), ("⑤ 구조전환", 2), ("마무리", 1)]
    h, start = "", 1
    for i, (t, n) in enumerate(segs):
        rng = f"{start}" if n == 1 else f"{start}~{start + n - 1}"
        h += f'<div class="dseg s{i}" style="--n:{n};--i:{i}"><b>{rng}</b><span>{e(t)}</span></div>'
        start += n
    return f'<div class="dbar">{h}</div>'


def mock():
    ring = "".join(f'<span style="--i:{i}">{t}</span>' for i, t in enumerate(("경제정상화", "혁신성장", "포용성장", "리스크 관리", "구조전환")))
    return ('<figure class="hmock"><div class="hbar"><i></i><i></i><i></i><span>발표자료.html</span></div><div class="hscr">'
            '<div class="hs h1"><small>2021.12.22 · 기획재정부</small><b>2022년 주요업무 추진계획</b><p>일상 회복 하에 선도형 경제로 도약</p></div>'
            f'<div class="hs h2"><b>5대 핵심 추진과제</b><div class="hring">{ring}</div></div>'
            '<div class="hs h3"><small>2022년 총지출</small><b class="hbig">607.7조원</b><div class="hgr"><i></i><i></i><i></i><i></i></div></div>'
            '</div><div class="hnav"><span>◀</span><em></em><span>▶</span></div><figcaption>예시 화면 (설명용 재현)</figcaption></figure>')


def m_deck():
    secs = [
        Sec(0, "보고서에서 발표장표까지 4단계", K,
            flow(("핵심 내용 정리", "보고서 첨부", "발표에 넣을 내용만"), ("장표별 내용 확정", "스타일·대상·시간은 내가", "장표마다 내용·화면·메시지"),
                 ("HTML 장표 만들기", "디자인 참고 자료 첨부", "이미지·도식·모션"), ("열어서 확인", "브라우저로 열기", "수치·출처 대조"))
            + call("‘장표 만들어줘’ 한 번이 아니라 — 내용 → 구성 → 디자인 순서로 나눠 요청한다") + source(CASE)),
        Sec(0, "1단계: 발표에 넣을 핵심 내용부터", K,
            pblock("A") + '<h5 class="lab">AI가 제안한 발표 흐름 (사례)</h5>'
            + chevrons("과거 성과", "경제여건", "정책 방향", "5대 핵심과제", "국민 체감 변화")
            + '<p class="dnote">원문 목차를 그대로 옮기지 않고, 듣는 사람이 따라오기 쉬운 흐름으로 다시 묶었습니다.</p>'),
        Sec(0, "2단계: 발표 조건은 내가 정하고 장표별 내용 확정", K,
            '<div class="i-split wide">' + pblock("B") + '<div class="col">' + options() + "</div></div>"),
        Sec(0, "예시: AI가 짠 20장 구성", K,
            plan_bar()
            + cards(card("장표마다 정리된 것", "포함할 내용", "제시할 수치", "화면 구성", "핵심 메시지"),
                    card("강조 순서도 제안", "5대 과제와 정책 방향을 가장 크게", "성과·여건은 필요성 근거로"),
                    card("주의", "수치는 보고서 작성 당시 전망·계획치", "실제 실적과 혼동하지 않기", dark=True))
            + source(CASE)),
        Sec(0, "3단계: 디자인 참고 자료를 주고 HTML로", K,
            '<div class="i-split wide">' + pblock("C") + '<div class="col">' + mock()
            + card("결과: HTML 파일 1개 (20장)", "방향키·버튼으로 넘기기", "전체 화면 · 진행률 표시") + "</div></div>"),
        Sec(0, "열어 보고 확인할 것", K,
            '<div class="i-split wide">' + check("발표 전 확인", ("수치", "원문과 같은가 · 전망·계획치를 실적처럼 쓰지 않았는가"),
                                                ("없는 내용", "보고서에 없는 효과·성과가 들어가지 않았는가"),
                                                ("이미지", "외부 이미지 주소는 인터넷이 있어야 보임 · 써도 되는 이미지인가"),
                                                ("열기", "Chrome·Edge로 열어 방향키·전체 화면 동작 확인"),
                                                ("보안", "그 보고서를 외부 AI에 올려도 되는가"))
            + card("디자인보다 확인이 먼저", "화려한 장표도 숫자 하나 틀리면 신뢰를 잃는다", "고칠 곳은 ‘어느 장표의 어느 수치’로 콕 집어 다시 요청", dark=True)
            + "</div>"),
    ]
    return Mod("deck", "보고서를 HTML 발표장표로 바꾸기", "25분", "시연 + 실습", "HTML 발표장표 1개", "ChatGPT",
               "완성한 보고서를 발표용 HTML 장표로 바꿉니다. 핵심 내용 정리 → 장표별 구성 확정 → 디자인 적용 순서로 나눠 요청합니다.", secs)


CSS = """
.dnote{font-size:14.5px;color:var(--mid)}
.dopts{display:flex;flex-direction:column;gap:10px}.dopt b{display:block;font-size:13.5px;color:var(--blue);margin-bottom:4px}
.dopt div{display:flex;flex-wrap:wrap;gap:6px}.dopt span{border:1px solid var(--line);border-radius:99px;padding:4px 12px;font-size:13.5px;background:#fff}
.dbar{display:flex;gap:4px;width:100%}.dseg{flex:var(--n);min-width:0;border-radius:10px;padding:10px 8px;color:#fff;background:var(--c);text-align:center}
.dseg b{display:block;font-size:13px;opacity:.85}.dseg span{display:block;font-size:13.5px;font-weight:600;line-height:1.3}
.s0{--c:#6f7077}.s1{--c:#55565c}.s2{--c:#0866d6}.s3{--c:#2f96f7}.s4{--c:#12a37a}.s5{--c:#f26a10}.s6{--c:#7b5cd6}.s7{--c:#26262a}
.hmock{margin:0;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff;box-shadow:0 6px 20px rgba(0,0,0,.08)}
.hbar{display:flex;align-items:center;gap:6px;background:#eceef1;padding:7px 10px}.hbar i{width:10px;height:10px;border-radius:50%;background:#c9ccd3}.hbar span{margin-left:8px;font-size:12px;color:var(--mid)}
.hscr{position:relative;height:200px;background:#fbfbfd}
.hs{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:6px;text-align:center;padding:12px;opacity:0;animation:hcyc 9s infinite}
.hs.h1{animation-delay:0s}.hs.h2{animation-delay:3s}.hs.h3{animation-delay:6s}
@keyframes hcyc{0%{opacity:0;transform:translateX(24px)}5%,30%{opacity:1;transform:none}36%,100%{opacity:0;transform:translateX(-24px)}}
.hs small{font-size:12px;color:var(--soft)}.hs b{font-size:21px;letter-spacing:-.02em}.hs p{font-size:13px;color:var(--mid)}
.hring{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;max-width:300px}.hring span{width:58px;height:58px;border-radius:50%;background:#e6f0fc;color:var(--blue);display:grid;place-items:center;font-size:11px;font-weight:700;line-height:1.2;padding:4px}
.hbig{font-size:34px!important;color:var(--blue)}.hgr{display:flex;gap:6px;align-items:flex-end;height:44px}.hgr i{width:16px;background:var(--blue);border-radius:3px 3px 0 0}
.hgr i:nth-child(1){height:40%}.hgr i:nth-child(2){height:55%}.hgr i:nth-child(3){height:70%}.hgr i:nth-child(4){height:100%;background:var(--orange)}
.hnav{display:flex;align-items:center;gap:8px;padding:6px 10px;border-top:1px solid var(--line);font-size:11px;color:var(--soft)}.hnav em{flex:1;height:4px;background:#e2e3e8;border-radius:2px;position:relative;overflow:hidden}
.hnav em:after{content:"";position:absolute;inset:0;background:var(--blue);transform-origin:left;animation:hprog 9s linear infinite}@keyframes hprog{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.hmock figcaption{font-size:12px;color:var(--soft);padding:0 10px 8px}
@media(max-width:680px){.dbar{flex-wrap:wrap}.dseg{flex:1 1 40%}}
"""

DECK_CSS = """
.slide .dnote{font-size:17px}.slide .dopt b{font-size:15px}.slide .dopt span{font-size:15.5px;padding:5px 14px}
.active .dopt span{animation:pop .35s ease both;animation-delay:calc(.4s + var(--i)*.08s)}
.slide .dseg{padding:16px 8px}.slide .dseg b{font-size:16px}.slide .dseg span{font-size:17px}
.dseg{transform-origin:left}.active .dseg{animation:growx .5s cubic-bezier(.2,.8,.2,1) both;animation-delay:calc(.15s + var(--i)*.14s)}
.slide .hscr{height:240px}.slide .hs b{font-size:25px}.slide .hs small{font-size:14px}.slide .hs p{font-size:15px}.slide .hring span{width:68px;height:68px;font-size:12.5px}.slide .hbig{font-size:42px!important}
.slide .chev li{font-size:19px;padding:14px 30px}
/* 강사소개 */
.slide.intro-slide{background:#fff;padding:0}
.ti{position:absolute;inset:0;overflow:hidden}
.ti-h{position:absolute;left:52px;top:26px;font-size:42px;font-weight:800;color:#2357d9;letter-spacing:-.02em}
.ti-tags{position:absolute;left:0;right:0;top:290px;display:flex;justify-content:center;gap:60px;font-size:68px;font-weight:800;color:#2357d9;transition:transform .8s cubic-bezier(.2,.8,.2,1)}
.ti-tags span{display:inline-block}
@keyframes tipop{0%{opacity:0;transform:scale(.3) rotate(-10deg)}100%{opacity:1;transform:none}}
.active .ti-tags span{animation:tipop .6s cubic-bezier(.3,1.6,.5,1) both;animation-delay:calc(.3s + var(--i)*.5s)}
.slide[data-step="1"] .ti-tags,.slide[data-step="2"] .ti-tags{transform:translateY(-205px) scale(.62)}
.ti-p{position:absolute;bottom:0;width:auto;border-radius:0;transform:translateY(105%);opacity:0;transition:transform .9s cubic-bezier(.25,1.25,.4,1),opacity .4s}
.ti-left{height:350px;left:150px}.ti-center{height:560px;left:525px;transition-delay:.15s}.ti-right{height:380px;left:880px;transition-delay:.3s}
.slide[data-step="1"] .ti-p,.slide[data-step="2"] .ti-p{transform:none;opacity:1}
.slide[data-step="2"] .ti-left{transform:translateX(-560px);opacity:0;transition-delay:0s}
.slide[data-step="2"] .ti-right{transform:translateX(560px);opacity:0;transition-delay:0s}
.slide[data-step="2"] .ti-center{transform:translateX(-400px);transition-delay:.2s}
.ti-name{position:absolute;left:800px;top:190px;font-size:88px;font-weight:300;color:#2357d9;line-height:1;opacity:0;transform:translateY(24px);transition:opacity .6s .7s,transform .7s .7s}
.ti-name b{font-size:56px;font-weight:800;color:#5aa63c;margin-left:14px}
.slide[data-step="1"] .ti-name{opacity:1;transform:none}
.slide[data-step="2"] .ti-name{opacity:1;transform:translateX(-220px);transition-delay:.25s}
.ti-list{position:absolute;left:600px;top:320px;display:grid;gap:9px;font-size:30px;font-weight:600;color:#1d1d20}
.ti-list li{display:flex;gap:14px;align-items:center;opacity:0;transform:translateX(36px);transition:opacity .45s,transform .45s}
.ti-list li:before{content:"";width:12px;height:12px;background:#e8582a;flex:none}
.slide[data-step="2"] .ti-list li{opacity:1;transform:none;transition-delay:calc(.7s + var(--i)*.16s)}
"""
