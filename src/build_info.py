"""python src/build_info.py → preview/info-source/index.html
추가 장표(AI 답변의 재료) 미리보기. docs/ 밖에 만들므로 배포되지 않는다."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build as B
import content_info as I
import lib


def main():
    lib.set_role("instructor")
    d = B.Deck()
    I.add(d)
    slides, n = d.render()
    base = "\n".join(l for l in B.CSS.splitlines() if not l.startswith("@media"))
    html = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI 답변의 재료 · 추가 장표 미리보기</title>{B.ROBOTS}{B.FONT}
<style>{base}
{B.DECK_CSS}{I.CSS}</style></head>
<body class="deckbody">
<div id="viewport"><div id="stage">{slides}</div></div>
<div id="bar"><button type="button" id="bprev" aria-label="이전">◀ 이전</button><button type="button" id="bnext" aria-label="다음">다음 ▶</button>
<span class="count" id="count" aria-live="polite">1 / {n}</span><div id="prog"><i id="progi"></i></div><span class="ttl" id="ttl"></span>
<button type="button" id="bover" title="O 키">전체 보기</button><button type="button" id="bfull" title="F 키">전체 화면</button></div>
<script>{B.DECK_JS}</script></body></html>
"""
    out = B.ROOT / "preview/info-source"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(html.replace('="../assets/', '="../../docs/assets/'), encoding="utf-8")
    print("built", out, n, "slides")


if __name__ == "__main__":
    main()
