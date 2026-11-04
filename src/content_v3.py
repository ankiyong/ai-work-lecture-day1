"""v3: 실습을 작업 하나씩 나눈 프롬프트(content_p)로 바꾼 판.
수강생: 신규 실습(공통 규칙 ~ ⑳ 초안) + 개정안 07~10.
강사: 개정안 01·02 → 신규 실습(프로세스 ~ 2-①) → 04 → 신규 2-②·3·초안 → 개정안 07·08 → 쉬어가기 → 09·10."""
import pathlib
import re

import content_a as A
import content_b as B
import content_deck as D
import content_c as X
import content_info as I
import content_p as P
import content_v2 as V
from lib import Mod, Sec, call, card, cards, flow, is_i, prompt, source
from motion import paths, stack

STEPS = ("보고서 흐름", ["규칙", "1", "2-①", "2-②", "3", "초안", "작성", "검토"])
BREAKS = {"09": V.BREAKS["09"]}
CSS = V.CSS + P.CSS + D.CSS + "\n.nm b{flex:none;white-space:nowrap}"  # 목차 번호(07·08)가 두 줄로 갈라지지 않게
JS = P.JS
DECK_JS = r"""
(function () {
  /* 영상 장: 장에 오면 처음부터 재생, 떠나면 멈춤, 끝나면 다음 장. 영상 위 클릭은 장 넘김으로 보내지 않는다 */
  [].forEach.call(document.querySelectorAll(".slide video[data-auto]"), function (v) {
    var sl = v.closest(".slide");
    ["click", "contextmenu", "touchstart", "touchend"].forEach(function (t) { v.addEventListener(t, function (e) { e.stopPropagation(); }); });
    new MutationObserver(function () {
      if (sl.classList.contains("active")) { v.currentTime = 0; var p = v.play(); if (p && p.catch) p.catch(function () {}); }
      else v.pause();
    }).observe(sl, { attributes: true, attributeFilter: ["class"] });
    v.addEventListener("ended", function () {
      if (sl.classList.contains("active")) document.dispatchEvent(new KeyboardEvent("keydown", { key: "ArrowRight" }));
    });
  });
})();
"""
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


def lean_ai():
    """생산 수단의 혁신: 리더보드 소개 화면 → 다음 클릭에 표로 바꾸고 1위 행을 강조한다."""
    body = ('<div class="lbshot"><img class="lb1" src="../assets/lean-ai-1.png" alt="Lean AI Native Companies Leaderboard 소개 화면: 1인 10억 달러 기업을 향한 흐름, 70개 기업 추적">'
            '<div class="lb2"><img src="../assets/lean-ai-2.png" alt="리더보드 표: 1위 Medvi, AI 원격진료, 직원 1명, 연매출 18억 달러">'
            '<span class="lbhi" aria-hidden="true"></span></div></div>')
    return Sec(0, "생성형 AI는 삶의 질 도구가 아니라 생산 수단의 혁신", KICK01, body + source("출처: LeanAILeaderboard.com (데이터 기준 2026년 10월)"),
               role="i", steps=1)


def vibe_coding():
    k = "01-4 · 우리는 어떻게 활용할 것인가?"
    return [
        Sec(0, "바이브코딩: 말로 설명하면 AI가 만들어 주는 시대", k,
            flow(("말로 설명", "무엇이 필요한지", "업무 언어 그대로"), ("AI가 코드 작성", "프로그램·자동화", "화면까지"),
                 ("실행해 보기", "결과를 직접 확인"), ("말로 고치기", "‘이 부분 바꿔 줘’", "될 때까지 반복"))
            + cards(card("업무에서", "반복되는 문서 정리·변환", "집계표·보고 양식 자동 채우기", "부서에 맞춘 작은 도구"),
                    card("일상에서", "가계부·일정 알림", "모임 안내 페이지", "나만 쓰는 계산기"),
                    card("누가 만드나", "코딩을 몰라도", "‘무엇이 필요한지’ 아는 사람이 만든다", dark=True))
            + source("바이브코딩(vibe coding): 2025년 2월 안드레이 카파시(Andrej Karpathy)가 처음 쓴 말"), role="i"),
        Sec(0, "사례: 공무원이 직접 만든 업무 도구 ‘범피스’", k,
            '<figure class="bpshot"><img src="../assets/bumpis.webp" alt="범정부오피스 1100일차 매뉴얼 표지, 범정부 오피스 소개, 개발자 인터뷰 기사"></figure>'
            + cards(card("범정부 오피스 (범피스)", "행정안전부에서 만든 문서 자동화 도구"),
                    card("무엇을 줄였나", "현장에서 반복되는 문서 편집 작업을 간소화"),
                    card("조직에 남긴 것", "공무원이 창의적이고 본질적인 행정업무에 집중하도록 지원", dark=True))
            + source("출처: 행정안전부 「범정부오피스 1100일차 매뉴얼」(2025.11) · 기사 「야근에 지친 공무원, ‘딸깍’으로 일터를 바꾸다」(2025.10.10, 이경수 행정안전부 행정제도과 주무관 인터뷰)"),
            role="i"),
    ]


def robot_video():
    """현장 로봇 장 앞의 영상. 장에 오면 처음부터 재생하고, 끝나면 다음 장으로 넘어간다 (DECK_JS)."""
    body = ('<div class="vplay"><div><small>01-2 · 이미 생긴 변화들</small><h2>“인간 VS 로봇”<br>10시간 택배 작업 대결</h2></div>'
            '<video data-auto src="../assets/video/robot-vs-human.mp4" controls playsinline preload="auto"></video>'
            '<span></span></div>')
    return Sec(0, "영상: 인간 VS 로봇 택배 작업 대결", "video-slide", body, role="i", kind="raw")


def m01():
    m, secs = A.m01(), []
    for s in m.secs:
        if s.title.startswith(("기획예산처는 AI 업무환경 선도 부처 ①", "단계 01")):
            continue
        if s.title.startswith("기획예산처는 AI 업무환경 선도 부처 ②"):
            s = brity()
        if s.title.startswith("현장도 바뀐다"):
            secs.append(robot_video())
        secs.append(s)
        if s.title == "어시스턴트와 에이전트의 경계":
            secs += [agent_case(), lean_ai()]
    m.secs = secs + vibe_coding()  # 01 끝, 02 마크다운 앞: 바이브코딩과 범피스 사례
    return m


# ── 07·08: 작성 스킬은 hwpx-writer를 그대로 쓴다 (수강생이 만들거나 정할 것 없음) ─────
SKILL_SRC = "근거: hwpx-writer 스킬 설명(SKILL.md)"


def m07():
    k = "07 · 작성 1~4 · 양식과 hwpx-writer"
    old = V.m07().secs  # 0 흐름, 1·2 HWPX 설명, 3 작성 1, 4 양식 확인, 5 작성 2, 6~8 스킬 만들기·이해 (교체)
    secs = [Sec(0, "양식 준비에서 스킬 만들기까지", k,
                flow(("빈 양식 받기", "양식1 HWPX", "양식2 HWP"), ("HWPX로 준비", "HWPX면 그대로", "HWP면 다른 이름으로 저장"),
                     ("스킬 이해", "스킬이란", "hwpx-writer가 하는 일"), ("스킬 만들기", "파일 또는 직접 입력", "hwpx-writer 내용 그대로"))
                + call("스킬 내용은 정해져 있다 — 내가 정하는 것은 보고서에 들어갈 내용이다"), step=["작성"])]
    secs += [V.rekick(s, k, ["작성"]) for s in old[1:5]]
    secs.append(V.rekick(old[5], k, ["작성"]))
    secs[-1].role = "i"  # 작성 2: HWPX로 저장하는 이유 — 강사 설명만
    secs.append(Sec(0, "작성 3: 스킬이란", k,
                    cards(card("스킬이란", "반복해서 쓸 작업 절차·규칙·도구를 묶은 것", "필요할 때 Claude가 꺼내 그대로 따른다"),
                          card("무엇으로 이루어지나", "이름·설명 — 언제 쓰는지", "지침(SKILL.md) — 어떻게 하는지", "필요하면 스크립트·참고 자료"),
                          card("프롬프트와 차이", "프롬프트: 이번 작업의 주제·자료·지시", "스킬: 여러 번 되풀이할 절차", "AI 재학습이 아님 · 판단은 계속 내가", dark=True))
                    + call("이번 실습의 스킬은 hwpx-writer — 한글(HWPX) 문서를 만들고 채우는 절차"), role="i", step=["작성"]))
    secs.append(Sec(0, "작성 3: hwpx-writer가 하는 일", k,
                    flow(("양식 분석", "받은 양식의 항목·표를 읽음", "원본은 보존"), ("내용 채우기", "주어진 내용을 항목에 배치", "기관명·연도 등은 추측하지 않음"),
                         ("파일 검사", "표·내용 보존 검사", "가능하면 한컴 화면으로 확인"), ("결과 보고", "수행한 검사·못 한 검사 구분", "초안은 완성본으로 넘기지 않음"))
                    + cards(card("HWP 양식이면", "Windows 한컴 환경에서 HWPX로 변환한 뒤 작업"),
                            card("내가 할 일", "결과 파일을 직접 열어 검토", "보고된 ‘못 한 검사’부터 확인", dark=True), n=2)
                    + source(SKILL_SRC), role="i", step=["작성"]))
    secs.append(Sec(0, "작성 4: 스킬을 만드는 두 가지 방법", k,
                    paths(("파일로 만들기", True, "스킬 파일 준비 (SKILL.md)", "Claude 스킬 메뉴에서 올리기", "목록에서 켜기"),
                          ("직접 입력", False, "이름·설명 입력", "지침 붙여 넣기", "목록에서 켜기"))
                    + cards(card("공통으로 필요한 것", "이름 · 설명 · 지침", "이번에는 hwpx-writer 내용 그대로"),
                            card("파일로 만들기", "SKILL.md를 그대로 올린다", "스크립트·참고 자료도 함께 담을 수 있다"),
                            card("직접 입력", "이름·설명·지침을 칸에 붙여 넣는다", "지침 글만 있으면 바로 만들 수 있다"))
                    + call("어느 방식이든 내용은 고치지 않는다 — 다음 장의 hwpx-writer를 그대로 쓴다"), step=["작성"]))
    secs.append(skill_practice(k))
    return Mod("07", "작성 1~4 · HWPX 양식과 hwpx-writer 스킬 만들기", "35분", "설명 + 실습", "빈 HWPX 양식 · hwpx-writer 스킬", "Claude",
               "기관의 빈 양식을 HWPX로 준비하고, 제공된 hwpx-writer 내용으로 Claude에 스킬을 만듭니다. 내용은 그대로 쓰며 따로 정할 것은 없습니다.", secs)


SKILL_FILE = pathlib.Path(__file__).resolve().parent.parent / "docs/assets/skills/hwpx-writer/SKILL.md"


def skill_parts():
    """SKILL.md → (이름, 설명, 본문, 본문의 ## 제목들)."""
    _, front, body = SKILL_FILE.read_text(encoding="utf-8").split("---", 2)
    meta = dict(re.findall(r'^(\w+):\s*"?(.*?)"?\s*$', front, re.M))
    body = body.strip()
    return meta["name"], meta["description"], body, re.findall(r"^## (.+)$", body, re.M)


def skill_practice(k):
    name, desc, body, heads = skill_parts()
    if is_i():
        html = ('<div class="i-split wide"><div class="col">'
                + card("만들 스킬", f"이름: {name}", f"설명: {desc}", "지침: SKILL.md 본문 그대로 (수강생 페이지에서 복사)", dark=True)
                + card("지침(SKILL.md)에 담긴 것", *heads) + '</div><div class="col">'
                + card("수강생이 할 일", "파일로 만들기: SKILL.md 내려받아 올리기", "직접 입력: 이름·설명·지침 붙여 넣기", "내용은 고치지 않는다")
                + card("강사 확인", "지침이 scripts/·references/의 파일을 부른다", "그 파일까지 있어야 그대로 동작한다", "수업 PC에서 스킬이 켜지는지 미리 확인")
                + "</div></div>" + source(SKILL_SRC))
    else:
        html = (prompt("스킬 이름", name, example=False) + prompt("설명", desc, example=False)
                + f'<details class="reveal"><summary>지침 전체 보기 · SKILL.md 본문 ({body.count(chr(10)) + 1}줄)</summary>'
                + prompt("지침 (SKILL.md 본문)", body, example=False) + "</details>"
                + '<p class="linkrow"><a class="btn link" href="assets/skills/hwpx-writer/SKILL.md" download="SKILL.md">SKILL.md 파일 내려받기</a></p>'
                + '<p class="tip">파일로 만들 때는 SKILL.md를 내려받아 올리고, 직접 입력할 때는 이름·설명·지침을 각각 복사해 붙여 넣습니다. 내용은 고치지 않습니다.</p>')
    return Sec(0, "작성 4 실습: hwpx-writer 스킬 만들기", k, html, step=["작성"])


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


DECK_CSS = V.DECK_CSS + I.CSS + P.DECK_CSS + D.DECK_CSS + """
.slide.video-slide{background:#111;padding:0}
.lbshot{width:960px;height:540px;margin:0 auto;position:relative;overflow:hidden;border-radius:12px;background:#fff;box-shadow:0 6px 24px rgba(0,0,0,.12)}
.lbshot img{display:block;width:100%;height:auto;border-radius:0}
.lb1{position:absolute;inset:0;transition:opacity .5s,transform .6s}
.lb2{position:absolute;left:0;right:0;top:50%;transform:translateY(-46%);opacity:0;transition:opacity .5s .15s,transform .6s .15s}
.lbhi{position:absolute;left:.4%;width:99.2%;top:15.6%;height:7.4%;border:4px solid #e8582a;border-radius:8px;box-shadow:0 0 0 9999px rgba(20,20,24,.38);opacity:0;transform:scale(1.08);transition:opacity .4s .8s,transform .4s .8s}
.slide[data-step="1"] .lb1{opacity:0;transform:scale(.97)}.slide[data-step="1"] .lb2{opacity:1;transform:translateY(-50%)}
.slide[data-step="1"] .lbhi{opacity:1;transform:none}
.bpshot{margin:0;text-align:center}.bpshot img{max-height:330px;width:auto;max-width:100%;border-radius:10px;border:1px solid var(--line)}
.vplay{position:absolute;inset:0;display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);align-items:center;gap:44px;padding:40px 52px}
.vplay video{height:640px;width:auto;border-radius:12px;background:#000;box-shadow:0 10px 40px rgba(0,0,0,.5)}
.vplay h2{color:#fff;font-size:36px;line-height:1.35;font-weight:700;text-align:right}.vplay small{display:block;text-align:right;color:var(--sky);font-size:17px;margin-bottom:10px}
.vplay p{color:#a9abb3;font-size:16px}
.agshot{width:960px;height:540px;margin:0 auto;position:relative;overflow:hidden;border-radius:12px;background:#111;box-shadow:0 6px 24px rgba(0,0,0,.18)}
.agz{position:absolute;inset:0;transform-origin:100% 23.2%;transition:transform .9s cubic-bezier(.2,.8,.2,1)}.agz img{width:100%;height:100%;display:block;border-radius:0}
.agf{position:absolute;left:80.6%;top:11.2%;width:19%;height:53%;border:4px solid var(--orange);border-radius:10px;transition:opacity .4s}
@keyframes agpulse{50%{box-shadow:0 0 0 8px rgba(242,106,16,.35)}}.active .agf{animation:agpulse 1.6s ease-in-out infinite}
.slide[data-step="1"] .agz{transform:scale(1.9)}.slide[data-step="1"] .agf{opacity:0}
.agnote{position:absolute;left:22px;bottom:22px;max-width:380px;background:rgba(38,38,42,.95);color:#fff;border-radius:12px;padding:16px 18px;opacity:0;transform:translateY(10px);transition:opacity .5s .6s,transform .5s .6s}
.slide[data-step="1"] .agnote{opacity:1;transform:none}.agnote b{display:block;color:var(--sky);font-size:16px}.agnote p{font-size:19px;line-height:1.45;margin-top:4px}.agnote .agsub{font-size:15px;color:#c9cad0}
"""


MD_EDITOR = "https://coddy.tech/tools/ko/markdown-editor"
MD_PROSE = ("민원 신청서 개선 회의 결과를 정리합니다. 회의는 11월 3일 민원실에서 열렸고 팀장과 담당 주무관 2명이 참석했습니다. "
            "논의 결과 세 가지를 하기로 했습니다. 첫째, 신청서 작성 예시를 새로 만듭니다. 둘째, 자주 틀리는 항목을 체크리스트로 정리합니다. "
            "셋째, 창구에 QR 안내문을 붙입니다. 다음 회의는 11월 17일입니다.")
MD_ANSWER = """# 민원 신청서 개선 회의 결과

- 일시: 11월 3일
- 장소: 민원실
- 참석: 팀장, 담당 주무관 2명

## 결정 사항
1. 신청서 작성 예시 새로 만들기
2. 자주 틀리는 항목을 **체크리스트**로 정리
3. 창구에 QR 안내문 붙이기

## 다음 회의
- 11월 17일"""


def md_practice():
    """수강생: 보고서 작성 프로세스 앞의 마크다운 실습 (에디터 주소 + 줄글 바꾸기 예제만)."""
    body = (f'<p class="linkrow"><a class="btn link" href="{MD_EDITOR}" target="_blank" rel="noopener">마크다운 에디터 열기</a> <small>{MD_EDITOR}</small></p>'
            + '<p>에디터를 열고 아래 줄글을 붙여 넣은 뒤, 제목(#)·목록(-, 1.)·굵게(**) 기호로 바꿔 봅니다. 미리보기에서 모양이 어떻게 바뀌는지 확인합니다.</p>'
            + prompt("줄글 예시 · 가상", MD_PROSE, example=False)
            + '<details class="reveal"><summary>바꿔 본 뒤 열어 보기: 예시 답안</summary>' + prompt("예시 답안", MD_ANSWER, example=False) + "</details>")
    return Sec(0, "마크다운 실습: 줄글을 마크다운으로 바꾸기", "실습 준비", body, role="s")


def intro_secs():
    if not is_i():
        return [md_practice()] + P.intro_secs()
    secs = [D.intro_slide()] + V.intro_secs()  # 표지 다음에 강사소개
    for s in secs:  # 개정안 단계 이름(2①)을 v3 지도 이름(2-①)으로, 작성 스킬은 hwpx-writer로
        if s.step:
            s.step = [str(x).replace("2①", "2-①").replace("2②", "2-②") for x in s.step]
        for a, b in INTRO_SWAP:
            s.body = s.body.replace(a, b)
    return secs


INTRO_SWAP = [
    ("작성 1~4 · HWPX 양식과 작성 스킬 만들기</td><td>설명 + 실습</td><td>빈 HWPX·작성 스킬",
     "작성 1~4 · HWPX 양식과 hwpx-writer 스킬 만들기</td><td>설명 + 실습</td><td>빈 HWPX 양식 · hwpx-writer 스킬"),
    ("작성 5 · 스킬로 보고서 작성", "작성 5 · hwpx-writer로 보고서 작성"),
    ("3~4  작성 스킬 만들고 이해", "3~4  hwpx-writer 스킬 이해·만들기"),
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
        tail = [m07(), write, gem, B.m10(), D.m_deck()]
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
