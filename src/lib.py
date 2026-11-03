"""강의안 HTML 부품. ROLE에 따라 강사용/수강생용 출력이 달라진다."""
from html import escape as e

ROLE = "instructor"


def set_role(r):
    global ROLE
    ROLE = r


def is_i():
    return ROLE == "instructor"


def only_s(*parts):
    """수강생 페이지에만 들어가는 내용."""
    return "" if is_i() else "".join(parts)


def only_i(*parts):
    """강사 페이지에만 들어가는 내용."""
    return "".join(parts) if is_i() else ""


def lines(*x):
    return "<ul>" + "".join(f"<li>{e(i)}</li>" for i in x if i) + "</ul>" if x else ""


def p(t, cls=""):
    return f'<p class="{cls}">{e(t)}</p>'


def source(t):
    return only_i(f'<p class="src">{e(t)}</p>')


def call(t):
    return f'<div class="call">{e(t)}</div>'


def card(title="", *items, big=None, unit="", tag="", dark=False, sub=""):
    h = ""
    if tag:
        h += f'<div class="tag">{e(tag)}</div>'
    if big:
        h += f'<div class="big">{e(big)}<small>{e(unit)}</small></div>'
    if title:
        h += f"<h4>{e(title)}</h4>"
    if sub:
        h += f'<div class="sub">{e(sub)}</div>'
    if items:
        h += lines(*items)
    return f'<div class="card{" dark" if dark else ""}">{h}</div>'


def raw_card(inner, dark=False):
    return f'<div class="card{" dark" if dark else ""}">{inner}</div>'


def cards(*c, n=3):
    return f'<div class="cards n{n}">{"".join(c)}</div>'


def flow(*steps):
    """steps: (제목, 항목...)"""
    h = ""
    for i, s in enumerate(steps, 1):
        h += f'<li style="--i:{i - 1}"><span class="dot">{i}</span><h4>{e(s[0])}</h4>{lines(*s[1:]) if len(s) > 1 else ""}</li>'
    return f'<ol class="flow n{len(steps)}">{h}</ol>'


def table(head, rows, hl_last=False):
    h = "".join(f"<th>{e(c)}</th>" for c in head)
    b = ""
    for i, r in enumerate(rows):
        cls = ' class="hl"' if hl_last and i == len(rows) - 1 else ""
        b += f"<tr{cls}>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>"
    return f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def bars(title, rows, cap=None):
    """rows: (이름, 값, 표시)"""
    m = max(r[1] for r in rows)
    b = "".join(
        f'<div class="bar"><span>{e(r[0])}</span><i><b style="width:{r[1] / m * 100:.1f}%"></b></i><em>{e(r[2])}</em></div>'
        for r in rows
    )
    c = f'<p class="muted">{e(cap)}</p>' if cap else ""
    return f'<div class="bars"><h5>{e(title)}</h5>{b}{c}</div>'


STEPS = None  # 개정안: (지도 이름, 단계 이름들). None이면 9단계 지도


def set_steps(s):
    global STEPS
    STEPS = s


def stepmap(*active):
    if STEPS:
        name, keys = STEPS
        on = {str(a) for a in active}
        d = "".join(f'<span class="{"on" if k in on else ""}">{e(k)}</span>' for k in keys)
        return f'<div class="stepmap v2" aria-label="{e(name)}, {e(", ".join(map(str, active)))} 진행 중"><small>{e(name)}</small>{d}</div>'
    d ="".join(f'<span class="{"on" if i in active else ""}">{i}</span>' for i in range(1, 10))
    return f'<div class="stepmap" aria-label="9단계 지도, {", ".join(map(str, active))}단계 진행 중"><small>9단계 지도</small>{d}</div>'


def prompt(label, text, example=True, tail=""):
    """예시 프롬프트: 수강생 페이지에서는 먼저 직접 쓰도록 접어 둔다."""
    body = (
        f'<div class="prompt"><div class="ph"><span>{e(label)}</span>'
        f'<button type="button" class="btn copy" data-copy>복사</button></div>'
        f"<pre>{e(text)}</pre>{tail}</div>"
    )
    if example and not is_i():
        return f'<details class="reveal"><summary>내 프롬프트를 쓴 뒤 열어 보기: {e(label)}</summary>{body}</details>'
    return body


def check(title, *items):
    """items: (항목, 질문)"""
    if is_i():
        h = "".join(f'<li style="--i:{n}"><span class="ok">✓</span><span><b>{e(i[0])}</b>{e(i[1])}</span></li>' for n, i in enumerate(items))
        return f'<div class="check show"><h5>{e(title)}</h5><ul>{h}</ul></div>'
    h = "".join(
        f'<li><label><input type="checkbox" data-k="chk:{e(title)}:{e(i[0])}"><span><b>{e(i[0])}</b>{e(i[1])}</span></label></li>'
        for i in items
    )
    return f'<div class="check"><h5>{e(title)}</h5><ul>{h}</ul></div>'


def fields(key, title, labels, rows=2):
    if is_i():
        h = ""
        for n, l in enumerate(labels):
            a, _, b = l.partition(" — ")
            d = f"<p>{e(b)}</p>" if b else ""
            h += f'<div class="card blank" style="--i:{n}"><h4>{e(a)}</h4>{d}<i></i></div>'
        c = 3 if len(labels) > 4 else 1
        return f'<div class="cards n{c}">{h}</div>'
    h = "".join(
        f'<label class="field"><span>{e(l)}</span><textarea rows="{rows}" data-k="{key}:{i}"></textarea></label>'
        for i, l in enumerate(labels)
    )
    return f'<div class="form" data-src="{key}" data-title="{e(title)}" data-kind="fields"><div class="fh"><h5>{e(title)}</h5><button type="button" class="btn" data-mdcopy>마크다운 복사</button></div>{h}</div>'


def form_table(key, title, head, rows, example=None, note=None):
    """rows: 첫 열 라벨. example: 첫 행 안내값(placeholder)."""
    if is_i():
        body = []
        for ri, lab in enumerate(rows):
            vals = list(example) if example and ri == 0 else [""] * (len(head) - 1)
            body.append([lab] + vals)
        n = f'<p class="muted">{e(note)}</p>' if note else ""
        return f'<h5 class="lab">{e(title)}</h5>' + table(head, body) + n
    th = "".join(f"<th>{e(c)}</th>" for c in head)
    b = ""
    for ri, lab in enumerate(rows):
        b += f"<tr><th scope=\"row\">{e(lab)}</th>"
        for ci in range(1, len(head)):
            ph = ""
            if example and ri == 0:
                ph = f' placeholder="{e(example[ci - 1])}"'
            b += f'<td><textarea rows="2"{ph} aria-label="{e(lab)} {e(head[ci])}" data-k="{key}:{ri}:{ci}"></textarea></td>'
        b += "</tr>"
    n = f'<p class="muted">{e(note)}</p>' if note else ""
    return (
        f'<div class="form" data-src="{key}" data-title="{e(title)}" data-kind="table"><div class="fh"><h5>{e(title)}</h5>'
        f'<button type="button" class="btn" data-mdcopy>마크다운 복사</button></div>'
        f'<div class="tw"><table class="ft"><thead><tr>{th}</tr></thead><tbody>{b}</tbody></table></div>{n}</div>'
    )


def fig(src, alt, cap=""):
    c = f"<figcaption>{e(cap)}</figcaption>" if cap else ""
    return f'<figure><img src="{src}" alt="{e(alt)}" loading="lazy">{c}</figure>'


class Sec:
    def __init__(self, pages, title, kicker, body, role="both", step=None, steps=0, kind="content"):
        self.steps, self.kind = steps, kind
        self.pages = pages if isinstance(pages, (list, tuple)) else [pages]
        self.title, self.kicker, self.body, self.role, self.step = title, kicker, body, role, step


class Mod:
    def __init__(self, num, title, time, method, result, tool, intro, secs, student_stub=None):
        self.num, self.title, self.time, self.method, self.result = num, title, time, method, result
        self.tool, self.intro, self.secs, self.student_stub = tool, intro, secs, student_stub
