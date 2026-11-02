"""슬라이드쇼 전용 도식. CSS 애니메이션은 slides.css가 맡는다."""
import math

from lib import e


def person(x, y, r=44, cls="pop", d=0):
    s = r / 44
    return (f'<g class="{cls}" style="--d:{d}"><g transform="translate({x} {y}) scale({s})">'
            '<circle r="44" fill="#26262a"/><circle cy="-13" r="14" fill="#fff"/>'
            '<path d="M-24 28c0-17 11-26 24-26s24 9 24 26z" fill="#fff"/><path d="M0 4l-5 9 5 14 5-14z" fill="#26262a"/></g></g>')


def robot(x, y, r=44, cls="pop", d=0):
    s = r / 44
    return (f'<g class="{cls}" style="--d:{d}"><g transform="translate({x} {y}) scale({s})">'
            '<circle r="44" fill="#0866d6"/><rect x="-21" y="-16" width="42" height="34" rx="7" fill="#fff"/>'
            '<rect x="-29" y="-6" width="5" height="14" rx="2" fill="#fff"/><rect x="24" y="-6" width="5" height="14" rx="2" fill="#fff"/>'
            '<rect x="-2" y="-27" width="4" height="11" fill="#fff"/><circle cy="-29" r="4" fill="#fff"/>'
            '<circle cx="-9" cy="-3" r="4" fill="#0866d6"/><circle cx="9" cy="-3" r="4" fill="#0866d6"/><rect x="-10" y="8" width="20" height="3" rx="1.5" fill="#0866d6"/></g></g>')


def line(x1, y1, x2, y2, d=0, cls="draw"):
    return f'<path class="{cls}" pathLength="1" style="--d:{d}" d="M{x1} {y1}L{x2} {y2}" marker-end="url(#ah)"/>'


DEFS = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0 0L10 5L0 10z" fill="#0866d6"/></marker></defs>')


def label(x, y, t, d=0, cls="fade", size=22):
    return f'<text class="{cls}" style="--d:{d}" x="{x}" y="{y}" text-anchor="middle" font-size="{size}" fill="#1d1d20">{e(t)}</text>'


def agent_scene():
    """16~22쪽: 다음 키로 1·2·3단계를 차례로 비춘다."""
    stages = [
        ("1 단계", "인간 – AI 어시스턴트 협업", "AI가 반복적인 업무를 보조해 인간의 효율을 높임"),
        ("2 단계", "인간 – AI 에이전트 협업", "에이전트가 팀의 디지털 동료로 합류해, 사람의 지시에 따라 전략 수립 등 구체적인 업무를 수행"),
        ("3 단계", "인간 주도, AI 에이전트 운영", "인간이 방향을 제시하면, 에이전트가 전체 업무 흐름을 주도하고 필요시 인간이 개입"),
    ]
    cards = "".join(f'<div class="card st st{i}"><div class="tag">{e(a)}</div><h4>{e(b)}</h4><p>{e(c)}</p></div>' for i, (a, b, c) in enumerate(stages, 1))
    p1 = (person(300, 130, 70) + robot(780, 130, 70, d=.2)
          + '<path class="flowline" d="M395 108H675" marker-end="url(#ah)"/><path class="flowline rev" d="M685 152H405" marker-end="url(#ah)"/>')
    p2 = person(540, 62, 50)
    for i, (x, t) in enumerate([(240, "자료조사"), (540, "기획"), (840, "문서화")]):
        d = .25 + i * .22
        p2 += line(540 + (x - 540) * .12, 116, x + (540 - x) * .08, 174, d) + robot(x, 214, 40, d=d + .3) + label(x, 284, t, d + .4)
    p3 = person(130, 140, 62) + label(305, 92, "업무지시", .2) + label(305, 215, "결과물", 1.3)
    p3 += '<path class="flowline" d="M215 118H395" marker-end="url(#ah)"/><path class="flowline rev" d="M400 164H220" marker-end="url(#ah)"/>'
    p3 += '<rect class="fade" x="425" y="10" width="620" height="260" rx="18" fill="#f4f5f7" stroke="#0866d6" stroke-width="2"/>'
    for i, (x, y) in enumerate([(535, 82), (735, 82), (935, 82), (535, 200), (735, 200), (935, 200)]):
        p3 += robot(x, y, 42, cls="pop bob", d=round(.3 + i * .12, 2))
    panels = "".join(f'<svg class="pn p{i}" viewBox="0 0 1080 300" role="img" aria-label="{e(stages[i - 1][1])} 도식">{DEFS}{x}</svg>' for i, x in enumerate((p1, p2, p3), 1))
    return f'<div class="agents"><div class="cards n3">{cards}</div><div class="panels">{panels}</div></div>'


def timeline(*items):
    """(시점, 제목, 항목...)"""
    h = ""
    for i, it in enumerate(items):
        ul = "".join(f"<li>{e(x)}</li>" for x in it[2:])
        h += f'<li style="--i:{i}"><b class="yr">{e(it[0])}</b><span class="tick"></span><div class="tc"><h4>{e(it[1])}</h4><ul>{ul}</ul></div></li>'
    return f'<ol class="timeline" style="--n:{len(items)}">{h}</ol>'


def chain(*items):
    """(작은 글씨, 큰 글씨, 강조)"""
    h = "".join(f'<li class="{"on" if x[2] else ""}" style="--i:{i}"><small>{e(x[0])}</small>{e(x[1])}</li>' for i, x in enumerate(items))
    return f'<ol class="chain">{h}</ol>'


def stack(tag, big, unit, items, hl, foot=""):
    rows = "".join(f'<li class="{"on" if x == hl else ""}" style="--i:{i}">{e(x)}</li>' for i, x in enumerate(items))
    f = f"<p>{e(foot)}</p>" if foot else ""
    return f'<div class="card dark stack"><div class="tag">{e(tag)}</div><div class="big">{e(big)}<small>{e(unit)}</small></div><ol>{rows}</ol>{f}</div>'


def exchange(a, b):
    return f'<div class="exchange">{a}<div class="swap" aria-hidden="true"><i>→</i><i>←</i></div>{b}</div>'


def hub():
    nodes = [("지메일", 0), ("드라이브", 0), ("캘린더", 0), ("지도", 0), ("유튜브", 0), ("노트북LM", 1), ("나노바나나 (이미지)", 1), ("Omni·Flow (영상)", 1)]
    cx, cy, h = 330, 200, ""
    for i, (t, kind) in enumerate(nodes):
        a = -math.pi / 2 + i * 2 * math.pi / len(nodes)
        x, y = cx + 235 * math.cos(a), cy + 150 * math.sin(a)
        d = round(.2 + i * .1, 2)
        col = "#f26a10" if kind else "#0866d6"
        h += f'<path class="draw plain" pathLength="1" style="--d:{d}" d="M{cx} {cy}L{x:.0f} {y:.0f}"/>'
        h += f'<g class="pop" style="--d:{d + .2:.2f}"><circle cx="{x:.0f}" cy="{y:.0f}" r="15" fill="{col}"/></g>'
        h += f'<text class="fade" style="--d:{d + .3:.2f}" x="{x:.0f}" y="{y + 36:.0f}" text-anchor="middle" font-size="19" fill="#1d1d20">{e(t)}</text>'
    h += f'<circle class="ring" cx="{cx}" cy="{cy}" r="58"/><g class="pop"><circle cx="{cx}" cy="{cy}" r="58" fill="#26262a"/></g><text x="{cx}" y="{cy + 8}" text-anchor="middle" font-size="24" fill="#fff" font-weight="600">Gemini</text>'
    return f'<div class="hubw"><h5>Gemini 연결 허브 <em class="k0">구글 서비스</em> <em class="k1">창작·정리 도구</em></h5><svg viewBox="0 0 660 400" role="img" aria-label="Gemini와 연결된 구글 서비스, 창작·정리 도구">{h}</svg></div>'


def chevrons(*names):
    h = "".join(f'<li style="--i:{i}">{e(n)}</li>' for i, n in enumerate(names))
    return f'<ol class="chev">{h}</ol>'


def doc_compare():
    messy = "".join(f'<rect class="mb" style="--i:{i}" x="{x}" y="{y}" width="{w}" height="{h}" rx="3"/>' for i, (x, y, w, h) in enumerate(
        [(14, 14, 90, 10), (14, 36, 64, 30), (84, 36, 62, 18), (14, 74, 40, 40), (60, 60, 54, 26), (120, 60, 26, 54), (60, 92, 54, 22)]))
    clean = '<rect class="cb" style="--i:0" x="14" y="14" width="80" height="11" rx="3"/>'
    for i, y in enumerate((38, 54, 70)):
        clean += f'<circle class="cb" style="--i:{i + 1}" cx="20" cy="{y + 4}" r="5"/><rect class="cg" style="--i:{i + 1}" x="34" y="{y}" width="{100 - i * 12}" height="8" rx="3"/>'
    for i in range(3):
        clean += f'<rect class="cb" style="--i:4" x="{14 + i * 46}" y="90" width="42" height="12" rx="2"/>'

    def row(cls, title, svg, res_t, items, status):
        li = "".join(f"<li>{e(x)}</li>" for x in items)
        return (f'<div class="drow {cls}"><h5>{e(title)}</h5><div class="dline"><svg class="doc" viewBox="0 0 160 124" aria-hidden="true">{svg}</svg>'
                f'<span class="pulse">→</span><svg class="bot" viewBox="-46 -46 92 92" aria-hidden="true">{robot(0, 0, 44, cls="")}</svg><span class="pulse">→</span>'
                f'<div class="card res"><h4><i>{status}</i>{e(res_t)}</h4><ul>{li}</ul></div></div></div>')
    return ('<div class="dcomp"><div>' + row("bad", "기존 HWP·PDF 문서", messy, "구조 인식이 어려움", ["복잡한 표·도식 → 구조 누락", "변환 과정이 먼저 필요"], "!")
            + row("good", "AI 친화 문서 (HWPX·마크다운)", clean, "구조대로 읽음", ["제목·번호·표를 구분해서 인식", "읽은 내용을 바로 활용"], "✓") + "</div>"
            + '<div class="card dark"><div class="tag">HWPX 알아두기</div><ol class="hw"><li style="--i:0">본문</li><li style="--i:1">서식·표</li><li style="--i:2">이미지</li></ol>'
            + "<ul><li>한글 문서의 개방형 형식</li><li>내용·서식이 구조화되어 저장</li><li>AI가 읽고 쓰기에 유리</li></ul></div></div>")


def paths(*rows):
    """(이름, 강조여부, 단계...)"""
    h, off = "", 0
    for name, on, *steps in rows:
        s = ""
        for st in steps:
            s += f'<li style="--i:{off}">{e(st)}</li>'
            off += 1
        h += f'<div class="path {"on" if on else ""}"><b>{e(name)}</b><ol>{s}</ol></div>'
    return f'<div class="paths">{h}</div>'


def inputs_scene():
    ins = [("보고서 기획안", "구조·목차"), ("근거 정리표", "내용·출처"), ("양식 (HWPX)", "서식")]
    a = "".join(f'<div class="card" style="--i:{i}"><h4>{e(x)}</h4><p>{e(y)}</p></div>' for i, (x, y) in enumerate(ins))
    return (f'<div class="ioscene"><div class="ins">{a}</div><span class="pulse">→</span>'
            '<div class="card dark tool"><span class="gear" aria-hidden="true">⚙</span><h4>작성 도구</h4><p>스킬 활용·미활용 경로</p></div><span class="pulse">→</span>'
            '<div class="card out"><span class="fileic" aria-hidden="true">HWPX</span><h4>HWPX 정책보고서 초안</h4><p>작성 → 확인 → 수정</p></div></div>')


def loopback():
    h, xs = "", {i: 70 + (i - 1) * 120 for i in range(1, 10)}
    for i, n in enumerate((8, 7, 6, 5, 4)):
        x1, x2 = xs[9], xs[n]
        top = 62 - i * 11
        h += f'<path class="draw" pathLength="1" style="--d:{round(.3 + i * .25, 2)}" d="M{x1} 74Q{(x1 + x2) / 2} {top - 40} {x2 + 5} 74" marker-end="url(#ah)"/>'
    for n, x in xs.items():
        cls = "on" if n >= 4 else ""
        h += f'<g class="lpn {cls} pop" style="--d:{n * .03:.2f}"><circle cx="{x}" cy="100" r="22"/><text x="{x}" y="107" text-anchor="middle" font-size="20">{n}</text></g>'
    return f'<svg class="loop" viewBox="0 0 1100 128" role="img" aria-label="9단계에서 4~8단계로 돌아가는 화살표">{DEFS}{h}</svg>'
