# AI와 함께하는 업무: 1일차 강의안

- 수강생 페이지: `docs/index.html` → 배포 주소 `/`
- 강사 슬라이드쇼: `docs/instructor/index.html` → 배포 주소 `/instructor/`
- 개정안 (보고서 흐름: 기획 3단계 → 작성 5단계 → 최종 검토): `docs/v2/` → 배포 주소 `/v2/`, `/v2/instructor/`

개정안은 모듈 03·05·06·07·08만 `src/content_v2.py`로 바꾸고 나머지 모듈은 기존 것을 그대로 씁니다. 예시 주제는 민원 신청서 보완요청 줄이기(가상)이며, 입력 저장은 기존 페이지와 따로 됩니다.

## 슬라이드쇼 조작

| 키 | 동작 |
|---|---|
| 왼쪽 클릭 · → · Space · PageDown | 다음 (단계가 있는 장은 다음 단계) |
| 오른쪽 클릭 · ← · PageUp | 이전 |
| F | 전체 화면 |
| O | 전체 보기, Esc로 닫기 |
| Home · End | 처음 · 끝 |

주소 끝 `#23`으로 특정 장을 바로 열 수 있습니다.

## 내용 수정

`src/`를 고친 뒤 다시 생성합니다. `docs/`의 HTML은 직접 고치지 않습니다.

```bash
python src/build.py
```

| 파일 | 내용 |
|---|---|
| `src/config.py` | 양식 파일, 영상·랭킹 사이트 주소, 수치 기준 시점 |
| `src/content_a.py` | 도입, 모듈 01·02·04 |
| `src/content_b.py` | 모듈 07·09·10 |
| `src/content_c.py` | 프롬프트 실습 모듈 03·05·06·08 |
| `src/builder.py` | 네 칸 프롬프트 입력 부품 (1 빈칸 채우기, 2 칸 채우기, 3 직접 설계) |
| `src/motion.py`, `src/slides.css` | 슬라이드 도식과 애니메이션 |

`Sec(..., role="i")`로 표시한 내용은 강사 슬라이드에만 나옵니다.

## 수업 전 확인

| 위치 | 확인할 일 |
|---|---|
| 시작 전 | Gemini·GPT 계정 로그인, 한글(HWPX) 열기 가능 여부 |
| 온AI·뉴시스 장 | 기사 캡처가 필요하면 원본 PPT 23~26쪽 사용 |
| 물류 로봇 장 | 영상 주소를 `config.py`에 입력 |
| 줄글 vs 구조화 프롬프트 | 두 방식을 직접 돌려 결과 확인 (미검증) |
| 미니 실습 | AI 화면에 마크다운 표가 표시되는지 확인 |
| 후보 요청 프롬프트 | 결과 확인 (미검증) |
| 랭킹 사이트 장 | 사이트 주소를 `config.py`에 입력 |
| 보고서 작성 | HWPX 양식 배부, 기관 PC의 스킬 실행 가능 여부 확인 |
| Gemini Notebook 질문 | 근거 위치 표시를 직접 실행해 확인 (미검증) |

발표자 노트(진행 시간과 멘트)는 슬라이드에 넣지 않았습니다. 원본 PPT에서 확인하세요.

## hwpx-writer 스킬 경로

`scripts/`와 `references/`를 포함한 스킬 폴더, Python을 실행할 수 있는 에이전트 도구가 필요합니다. 한컴 페이지 렌더링 확인에는 Windows 한컴오피스가 필요합니다. 설치가 막히면 스킬 경로는 강사 시연으로 진행하고, 수강생은 미활용 경로로 완주합니다.

스킬 폴더 기준 양식 채우기 명령입니다.

```text
python scripts/fill_hwpx.py analyze form.hwpx
python scripts/fill_hwpx.py fill form.hwpx filled.hwpx --values values.json
python scripts/fill_hwpx.py check filled.hwpx --strict
python scripts/render_hwpx.py C:/절대경로/filled.hwpx --output-dir C:/절대경로/비어있는-새폴더
```

`published: false` 후보는 완성본으로 전달하지 않습니다. 정적 검사 통과, 한컴 열림, 렌더 성공, 눈으로 확인은 서로 다른 단계입니다.

## GitHub Pages 배포

저장소 Settings → Pages에서 Source를 `Deploy from a branch`, 폴더를 `/docs`로 지정합니다.

강사 페이지는 메뉴 연결이 없고 검색 차단이 걸려 있지만, 주소를 아는 사람은 열 수 있습니다.
