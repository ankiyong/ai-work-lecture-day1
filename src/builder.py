"""네 칸 프롬프트 빌더. 단계가 올라갈수록 제공하는 내용을 줄인다.

1단계(빈칸 채우기) 템플릿 문법:
  [[이름|안내|기본값]]  한 줄 빈칸
  [[#이름|안내]]        여러 줄 빈칸
  {{s04}}               앞 단계 결과 자동 입력 칸 (수강생 페이지의 data-src 값)
"""
import re

from lib import e, is_i

SLOTS = ("자료", "요청", "출력 형식", "규칙·기타")
LEVELS = {1: "1단계 · 빈칸 채우기", 2: "2단계 · 칸 채우기", 3: "3단계 · 직접 설계"}
SRC_NAMES = {
    "s01": "단계 01 기록", "s02c": "주제 카드", "s04": "근거 정리표", "s05r": "단계 05 결과",
    "s06r": "판단 ② 대안 비교표", "s07r": "판단 ③ 추진계획", "s08r": "판단 ④ 기대효과", "s0o": "보고서 개요",
}
TOKEN = re.compile(r"(\[\[.*?\]\]|\{\{.*?\}\}|\n)")


def _auto(key, src):
    name = SRC_NAMES[src]
    return (f'<span class="autow"><textarea rows="3" data-k="{key}" data-from="{src}" aria-label="{e(name)} 자동 입력" '
            f'placeholder="{e(name)}을(를) 채우면 자동으로 들어옵니다. 직접 붙여 넣어도 됩니다."></textarea>'
            f'<button type="button" class="btn" data-refill>다시 가져오기</button></span>')


def _template(key, slot_i, text):
    """1단계 템플릿 → 수강생 입력 칸 / 슬라이드 표시."""
    out, n = "", 0
    for part in TOKEN.split(text):
        if not part:
            continue
        if part == "\n":
            out += "<br>"
        elif part.startswith("{{"):
            src = part[2:-2]
            if is_i():
                out += f'<span class="blk auto">{e(SRC_NAMES[src])} 자동 입력</span>'
            else:
                out += _auto(f"{key}:{slot_i}:{n}", src)
                n += 1
        elif part.startswith("[["):
            bits = part[2:-2].split("|") + ["", ""]
            name, hint, default = bits[0], bits[1], bits[2]
            multi = name.startswith("#")
            name = name.lstrip("#")
            if is_i():
                out += f'<span class="blk">{e(default or name)}</span>'
            elif multi:
                out += f'<textarea rows="3" class="bk" data-k="{key}:{slot_i}:{n}" data-blank="{e(name)}" aria-label="{e(name)}" placeholder="{e(hint or name)}"></textarea>'
                n += 1
            else:
                w = max(len(default or hint or name) * 1.6, 8)
                out += (f'<input type="text" class="bk" style="width:min({w:.0f}ch,100%)" data-k="{key}:{slot_i}:{n}" data-blank="{e(name)}" '
                        f'aria-label="{e(name)}" placeholder="{e(hint or name)}" value="{e(default)}">')
                n += 1
        else:
            out += e(part)
    return out


def _srcs(srcs):
    if not srcs or is_i():
        return ""
    return '<div class="srcs">' + "".join(f'<button type="button" class="btn" data-srccopy="{s}">{e(SRC_NAMES[s])} 복사</button>' for s in srcs) + "</div>"


def _extras(extras):
    if not extras:
        return ""
    return '<div class="opts"><small>넣을 수 있는 것</small>' + "".join(f"<span>{e(x)}</span>" for x in extras) + "</div>"


def builder(key, level, goal, slots, extras=(), tip="", srcs=(), auto=None):
    """slots: (자료, 요청, 출력 형식, 규칙). 1단계는 템플릿, 2·3단계는 힌트."""
    head = f'<div class="bh"><span class="lv lv{level}">{e(LEVELS[level])}</span><p>{e(goal)}</p></div>'
    if is_i():
        return _slide(head, level, slots, extras, tip, key, auto)
    body = _srcs(srcs)
    if level == 3:
        hints = "".join(f"<li><b>{SLOTS[i]}</b> {e(h)}</li>" for i, h in enumerate(slots))
        body += (f'<textarea rows="8" class="free" data-k="{key}:free" data-free aria-label="내 프롬프트" placeholder="자료 / 요청 / 출력 형식 / 규칙·기타 네 칸을 떠올리며 직접 씁니다."></textarea>'
                 f'<details class="hint"><summary>막히면 칸별 힌트 보기</summary><ul>{hints}</ul></details>')
    else:
        for i, name in enumerate(SLOTS):
            if level == 1:
                v = f'<div class="sv">{_template(key, i, slots[i])}</div>'
            elif i == 0 and auto:
                v = f'<div class="sv">{_auto(f"{key}:{i}", auto)}</div>'
            else:
                v = f'<div class="sv"><textarea rows="2" data-k="{key}:{i}" aria-label="{name}" placeholder="{e(slots[i])}"></textarea></div>'
            etc = ""
            if i == 3 and level == 1:
                etc = f'<label class="etc"><span>기타 추가사항 (선택)</span><textarea rows="1" data-k="{key}:etc" data-etc></textarea></label>'
            body += f'<div class="slot" data-slot="{name}"><b>{name}</b><div class="sc">{v}{etc}</div></div>'
    body += _extras(extras)
    if tip:
        body += f'<p class="tip">{e(tip)}</p>'
    if level == 3:
        out = '<div class="bfoot"><button type="button" class="btn pri" data-bcopy>내 프롬프트 복사</button></div>'
    else:
        out = '<div class="bout"><div class="ph"><span>완성 프롬프트</span><button type="button" class="btn copy" data-bcopy>복사</button></div><pre data-out></pre></div>'
    return f'<div class="builder" data-level="{level}">{head}{body}{out}</div>'


def _slide(head, level, slots, extras, tip, key, auto):
    if level == 3:
        cells = "".join(f'<div class="cell empty" style="--i:{i}"><b>{SLOTS[i]}</b><i></i></div>' for i in range(4))
        msg = '<p class="tip">목표만 보고 네 칸을 직접 설계합니다. 막히면 칸별 힌트와 예시를 엽니다.</p>'
    else:
        cells = ""
        for i, name in enumerate(SLOTS):
            if level == 1:
                v = _template(key, i, slots[i])
                if i == 3:
                    v += '<span class="etcline">+ 기타 추가사항</span>'
            elif i == 0 and auto:
                v = f'<span class="blk auto">{e(SRC_NAMES[auto])} 자동 입력</span>'
            else:
                v = f'<span class="hintv">{e(slots[i])}</span>'
            cells += f'<div class="cell" style="--i:{i}"><b>{name}</b><div>{v}</div></div>'
        msg = f'<p class="tip">{e(tip)}</p>' if tip else ""
    return f'<div class="four">{head}<div class="cells">{cells}</div>{_extras(extras)}{msg}</div>'
