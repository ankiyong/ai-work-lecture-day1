"""v3: 실습을 작업 하나씩 나눈 프롬프트(content_p)로 바꾼 판.
수강생: 신규 실습(공통 규칙 ~ ⑳ 초안) + 개정안 07~10.
강사: 개정안 01·02 → 신규 실습(프로세스 ~ 2-①) → 04 → 신규 2-②·3·초안 → 개정안 07·08 → 쉬어가기 → 09·10."""
import content_a as A
import content_b as B
import content_info as I
import content_p as P
import content_v2 as V
from lib import is_i

STEPS = ("보고서 흐름", ["규칙", "1", "2-①", "2-②", "3", "초안", "작성", "검토"])
BREAKS = {"09": V.BREAKS["09"]}
CSS = V.CSS + P.CSS
DECK_CSS = V.DECK_CSS + I.CSS + P.DECK_CSS
JS = P.JS


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
    md, write, gem = A.m02(), V.m08(), B.m09()
    tail = [V.m07(), write, gem, B.m10()]
    if is_i():
        mods = [A.m01(), md, P.m0(), P.m1(), P.m21(), A.m04(), P.m22(), P.m3(), P.m_draft()] + tail
    else:
        mods = P.modules() + tail
    for k, m in enumerate(mods, 1):
        m.num = f"{k:02d}"
    BREAKS.clear()
    BREAKS[gem.num] = V.BREAKS["09"]
    EXTRA.clear()
    EXTRA.update({md.num: after_md, write.num: I.add})
    return mods
