"""v3: 실습을 작업 하나씩 나눈 프롬프트(content_p)로 바꾼 판.
수강생: 신규 실습(공통 규칙 ~ ⑳ 초안) + 개정안 07~10.
강사: 개정안 01·02 → 신규 실습(프로세스 ~ 2-①) → 04 → 신규 2-②·3·초안 → 개정안 07·08 → 쉬어가기 → 09·10."""
import content_a as A
import content_b as B
import content_c as X
import content_info as I
import content_p as P
import content_v2 as V
from lib import Sec, card, is_i, source
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
    for s in secs:  # 개정안 단계 이름(2①)을 v3 지도 이름(2-①)으로
        if s.step:
            s.step = [str(x).replace("2①", "2-①").replace("2②", "2-②") for x in s.step]
    return secs


def after_md(d):
    """강사: 마크다운 다음에 신규 실습 프로세스 장."""
    for s in P.intro_secs():
        d.content(s)


EXTRA = {}  # 모듈 번호 → 그 모듈 뒤에 장을 더하는 함수. 번호가 연번으로 바뀌므로 modules()가 채운다


def modules():
    """페이지마다 01부터 연번. 쉬어가기는 보고서 작성·최종 검토 뒤, 휴식은 Gemini Notebook 앞에 둔다."""
    X.FORMS = FORMS  # 07·08의 양식 내려받기 버튼을 양식1·양식2로
    try:
        md, write, gem = A.m02(), V.m08(), B.m09()
        tail = [V.m07(), write, gem, B.m10()]
    finally:
        X.FORMS = ()
    if is_i():
        mods = [m01(), md, P.m0(), P.m1(), P.m21(), A.m04(), P.m22(), P.m3(), P.m_draft()] + tail
    else:
        mods = P.modules() + tail
    for k, m in enumerate(mods, 1):
        m.num = f"{k:02d}"
    BREAKS.clear()
    BREAKS[gem.num] = V.BREAKS["09"]
    EXTRA.clear()
    EXTRA.update({md.num: after_md, write.num: I.add})
    return mods
