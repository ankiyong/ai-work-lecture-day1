"""python src/build_practice.py → preview/practice/index.html(수강생), preview/practice/instructor/index.html(강사)
실습 개정안(작업 하나씩 나눈 프롬프트) 미리보기. docs/ 밖에 만들므로 배포되지 않는다."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build as B
import content_p as P
import content_v2 as V
import lib

VP = B.Ver("", P.intro_secs, P.modules, {}, "eid-pr:", " · 실습 개정안", P.STEPS, V.CSS + P.CSS, V.DECK_CSS + P.DECK_CSS, js=P.JS)


def main():
    out = B.ROOT / "preview/practice"
    (out / "instructor").mkdir(parents=True, exist_ok=True)
    s, i = B.student_page(VP), B.deck_page(VP)
    lib.set_steps(None)
    (out / "index.html").write_text(s.replace('="assets/', '="../../docs/assets/'), encoding="utf-8")
    (out / "instructor/index.html").write_text(i.replace('="../assets/', '="../../../docs/assets/'), encoding="utf-8")
    print("built", out)


if __name__ == "__main__":
    main()
