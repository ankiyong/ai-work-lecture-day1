"""v3: 실습을 작업 하나씩 나눈 프롬프트(content_p)로 바꾼 판.
수강생: 신규 실습(공통 규칙 ~ ⑳ 초안) + 개정안 07~10.
강사: 개정안 01·02 → 신규 실습(프로세스 ~ 2-①) → 04 → 신규 2-②·3·초안 → 개정안 07·08 → 쉬어가기 → 09·10."""
import content_a as A
import content_b as B
import content_c as X
import content_info as I
import content_p as P
import content_v2 as V
from lib import Mod, Sec, call, card, cards, flow, is_i, source
from motion import stack

STEPS = ("보고서 흐름", ["규칙", "1", "2-①", "2-②", "3", "초안", "작성", "검토"])
BREAKS = {"09": V.BREAKS["09"]}
CSS = V.CSS + P.CSS
JS = P.JS
KICK01 = "01-3 · 앞으로 달라질 업무"
FORMS = (("양식1 내려받기 · HWPX", "assets/forms/form1.hwpx", "기획예산처_업무보고서_양식.hwpx"),
         ("양식2 내려받기 · HWP", "assets/forms/form2.hwp", "기획예산처_업무보고서_양식.hwp"))


# ── 01 모듈: 에이전트 실제 사례 추가, 기획예산처 한정 장 정리 ─────────
def agent_case():
    """처음엔 화면 전체, 다음 클릭에 오른쪽 봇 목록을 확대한다."""
    body = ('<div class="agshot"><div class="agz"><img src="../assets/agent-team.webp" '
            'alt="Discord 업무 서버 화면: 채널별로 일정·문서화 등 업무를 나누고, 오른쪽 목록에 AI 에이전트 봇 7개와 관리자가 있다">'
            '<span class="agf" aria-hidden="true"></span></div>'
            '<div class="agnote"><b>Discord 서버 하나 = AI 팀</b><p>에이전트 봇 7개가 각자 맡은 일을 하고, 나는 지시하고 승인합니다.</p>'
            '<p class="agsub">예: Karina = 일정 담당(scheduler)</p></div></div>')
    return Sec(0, "실제 사례: 내가 쓰는 AI 에이전트 팀", KICK01, body, role="i", steps=1)


def brity():
    return Sec(0, "공공기관에 Brity Works 도입", KICK01,
               '<div class="split">' + card("브리티웍스, 중앙부처 9곳 도입", "행안부 '온AI' 공식 협업 도구", "4월 첫 도입 후 8월까지 순차 서비스")
               + stack("Brity Works 도입", "9개", "부처", ["재정경제부·기획예산처", "국가보훈부·산업통상부", "고용노동부·금융위원회", "재외동포청 등"], "",
                       "공공 업무에 AI 협업 도구가 들어오고 있다") + "</div>"
               + source("출처: 삼성SDS 보도 「브리티웍스, 중앙부처 9곳 도입…정부 AI 행정혁신 가속」(2026.8.13)"), role="i")


def m01():
    m, secs = A.m01(), []
    for s in m.secs:
        if s.title.startswith(("기획예산처는 AI 업무환경 선도 부처 ①", "단계 01")):
            continue
        if s.title.startswith("기획예산처는 AI 업무환경 선도 부처 ②"):
            s = brity()
        secs.append(s)
        if s.title == "어시스턴트와 에이전트의 경계":
            secs.append(agent_case())
    m.secs = secs
    return m


# ── 07·08: 작성 스킬은 hwpx-writer를 그대로 쓴다 (수강생이 만들거나 정할 것 없음) ─────
SKILL_SRC = "근거: hwpx-writer 스킬 설명(SKILL.md)"


def m07():
    k = "07 · 작성 1~4 · 양식과 hwpx-writer"
    old = V.m07().secs  # 0 흐름, 1·2 HWPX 설명, 3 작성 1, 4 양식 확인, 5 작성 2, 6~8 스킬 만들기·이해 (교체)
    secs = [Sec(0, "양식 준비에서 스킬 적용 준비까지", k,
                flow(("빈 양식 받기", "양식1 HWPX", "양식2 HWP"), ("HWPX로 준비", "HWPX면 그대로", "HWP면 다른 이름으로 저장"),
                     ("hwpx-writer 확인", "제공된 스킬 그대로", "따로 정할 것 없음"), ("스킬이 하는 일 보기", "분석 · 채우기", "검사 · 보고"))
                + call("스킬은 정해져 있다 — 내가 정하는 것은 보고서에 들어갈 내용이다"), step=["작성"])]
    secs += [V.rekick(s, k, ["작성"]) for s in old[1:6]]
    secs.append(Sec(0, "작성 3: hwpx-writer 스킬을 그대로 쓴다", k,
                    cards(card("제공된 스킬", "이름: hwpx-writer (한글 문서 만들기)", "강사가 준비한 내용을 그대로 사용", "수강생이 만들거나 고칠 것 없음", dark=True),
                          card("내가 확인할 것", "Claude에서 hwpx-writer를 쓸 수 있는가", "빈 양식(양식1 HWPX 또는 양식2 HWP)을 받았는가"),
                          card("내가 정할 것", "보고서에 들어갈 내용뿐", "확정한 기획안 초안(⑳) · 확인 기록 · 빈 양식을 함께 준다"))
                    + call("스킬 설정은 건드리지 않는다 — 내 몫은 내용과 최종 확인"), step=["작성"]))
    secs.append(Sec(0, "작성 4: hwpx-writer가 하는 일", k,
                    flow(("양식 분석", "받은 양식의 항목·표를 읽음", "원본은 보존"), ("내용 채우기", "주어진 내용을 항목에 배치", "기관명·연도 등은 추측하지 않음"),
                         ("파일 검사", "표·내용 보존 검사", "가능하면 한컴 화면으로 확인"), ("결과 보고", "수행한 검사·못 한 검사 구분", "초안은 완성본으로 넘기지 않음"))
                    + cards(card("HWP 양식이면", "Windows 한컴 환경에서 HWPX로 변환한 뒤 작업"),
                            card("내가 할 일", "결과 파일을 직접 열어 검토", "보고된 ‘못 한 검사’부터 확인", dark=True), n=2)
                    + source(SKILL_SRC), step=["작성"]))
    return Mod("07", "작성 1~4 · HWPX 양식과 hwpx-writer 스킬", "35분", "설명 + 실습", "빈 HWPX 양식 · 스킬 사용 준비", "Claude",
               "기관의 빈 양식을 HWPX로 준비하고, 제공된 hwpx-writer 스킬이 무엇을 하는지 확인합니다. 스킬은 그대로 쓰며 따로 정할 것은 없습니다.", secs)


M08_SWAP = [  # 기존 개정안 08의 스킬 이름·스킬 만들기 흔적을 hwpx-writer 기준으로
    ("&#x27;공공 보고서 HWPX 작성&#x27; 스킬", "hwpx-writer 스킬"),
    ("Claude · 공공 보고서 HWPX 작성", "Claude · hwpx-writer"),
    ("<td>작성 3</td><td>스킬 규칙 보완 뒤 다시 작성</td>", "<td>작성 5</td><td>깨진 위치를 알려 주고 다시 작성 요청</td>"),
    ("<h4>재사용할 작성 스킬</h4><ul><li>내가 정한 작성 기준</li>", "<h4>HWPX 양식 + hwpx-writer 작성 절차</h4><ul><li>스킬은 그대로, 내용만 바꿔서</li>"),
]


def m08():
    m = V.m08()
    m.title = m.title.replace("스킬로", "hwpx-writer로")
    m.intro = m.intro.replace("작성 스킬을", "hwpx-writer 스킬을")
    hits = {a: 0 for a, _ in M08_SWAP}
    for s in m.secs:
        s.title = s.title.replace("스킬로 보고서 작성", "hwpx-writer로 보고서 작성")
        for a, b in M08_SWAP:
            hits[a] += s.body.count(a)
            s.body = s.body.replace(a, b)
    missed = [a for a, n in hits.items() if not n]
    assert not missed, f"08 바꿀 문구를 찾지 못함: {missed}"
    return m


DECK_CSS = V.DECK_CSS + I.CSS + P.DECK_CSS + """
.agshot{width:960px;height:540px;margin:0 auto;position:relative;overflow:hidden;border-radius:12px;background:#111;box-shadow:0 6px 24px rgba(0,0,0,.18)}
.agz{position:absolute;inset:0;transform-origin:100% 23.2%;transition:transform .9s cubic-bezier(.2,.8,.2,1)}.agz img{width:100%;height:100%;display:block;border-radius:0}
.agf{position:absolute;left:80.6%;top:11.2%;width:19%;height:53%;border:4px solid var(--orange);border-radius:10px;transition:opacity .4s}
@keyframes agpulse{50%{box-shadow:0 0 0 8px rgba(242,106,16,.35)}}.active .agf{animation:agpulse 1.6s ease-in-out infinite}
.slide[data-step="1"] .agz{transform:scale(1.9)}.slide[data-step="1"] .agf{opacity:0}
.agnote{position:absolute;left:22px;bottom:22px;max-width:380px;background:rgba(38,38,42,.95);color:#fff;border-radius:12px;padding:16px 18px;opacity:0;transform:translateY(10px);transition:opacity .5s .6s,transform .5s .6s}
.slide[data-step="1"] .agnote{opacity:1;transform:none}.agnote b{display:block;color:var(--sky);font-size:16px}.agnote p{font-size:19px;line-height:1.45;margin-top:4px}.agnote .agsub{font-size:15px;color:#c9cad0}
"""


def intro_secs():
    if not is_i():
        return P.intro_secs()
    secs = V.intro_secs()
    for s in secs:  # 개정안 단계 이름(2①)을 v3 지도 이름(2-①)으로, 작성 스킬은 hwpx-writer로
        if s.step:
            s.step = [str(x).replace("2①", "2-①").replace("2②", "2-②") for x in s.step]
        for a, b in INTRO_SWAP:
            s.body = s.body.replace(a, b)
    return secs


INTRO_SWAP = [
    ("작성 1~4 · HWPX 양식과 작성 스킬 만들기</td><td>설명 + 실습</td><td>빈 HWPX·작성 스킬",
     "작성 1~4 · HWPX 양식과 hwpx-writer 스킬</td><td>설명 + 실습</td><td>빈 HWPX 양식 · 스킬 사용 준비"),
    ("작성 5 · 스킬로 보고서 작성", "작성 5 · hwpx-writer로 보고서 작성"),
    ("3~4  작성 스킬 만들고 이해", "3~4  hwpx-writer 스킬 확인"),
    ("5  스킬로 보고서 작성", "5  hwpx-writer로 보고서 작성"),
    ("재사용할 작성 스킬", "HWPX 양식 + hwpx-writer 작성 절차"),
]


def after_md(d):
    """강사: 마크다운 다음에 신규 실습 프로세스 장."""
    for s in P.intro_secs():
        d.content(s)


EXTRA = {}  # 모듈 번호 → 그 모듈 뒤에 장을 더하는 함수. 번호가 연번으로 바뀌므로 modules()가 채운다


def modules():
    """페이지마다 01부터 연번. 쉬어가기는 보고서 작성·최종 검토 뒤, 휴식은 Gemini Notebook 앞에 둔다."""
    X.FORMS = FORMS  # 07·08의 양식 내려받기 버튼을 양식1·양식2로
    try:
        md, write, gem = A.m02(), m08(), B.m09()
        tail = [m07(), write, gem, B.m10()]
    finally:
        X.FORMS = ()
    if is_i():
        mods = [m01(), md, P.m0(), P.m1(), P.m21(), A.m04(), P.m22(), P.m3(), P.m_draft()] + tail
    else:
        mods = P.modules() + tail
        for m in mods:  # 수강생 페이지에는 '확인:'·'점검:' 장을 두지 않는다
            m.secs = [s for s in m.secs if not s.title.startswith(("확인:", "점검:"))]
    for k, m in enumerate(mods, 1):
        m.num = f"{k:02d}"
    BREAKS.clear()
    BREAKS[gem.num] = V.BREAKS["09"]
    EXTRA.clear()
    EXTRA.update({md.num: after_md, write.num: I.add})
    return mods
