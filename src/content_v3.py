"""v3: 실습을 작업 하나씩 나눈 프롬프트(content_p)로 바꾼 판.
수강생: 신규 실습(공통 규칙 ~ ⑳ 초안) + 개정안 07~10.
강사: 개정안 01·02 → 쉬어가기 → 신규 실습(프로세스 ~ 2-①) → 04 → 신규 2-②·3·초안 → 개정안 07~10."""
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


def after_02(d):
    """강사: 마크다운 다음에 쉬어가기, 이어서 신규 실습 프로세스 장."""
    I.add(d)
    for s in P.intro_secs():
        d.content(s)


def modules():
    tail = [V.m07(), V.m08(), B.m09(), B.m10()]
    if is_i():
        return [A.m01(), A.m02(), P.m0(), P.m1(), P.m21(), A.m04(), P.m22(), P.m3(), P.m_draft()] + tail
    return P.modules() + tail
