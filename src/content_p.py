"""실습 개정안: 프롬프트 하나가 작업 하나를 하고 결과물 하나를 낸 뒤 멈춘다.
필수: 공통 규칙, 1단계(①~④), 2-②(⑧~⑩). 선택: 2-①(⑤~⑦), 3(⑪~⑲)은 진행 순서를 보고 체크한 작업만 펼친다.

프롬프트 빈칸 문법:
  [[#이름|비었을 때 남길 글|입력 예시]]  여러 줄 빈칸 (같은 줄 앞 글자 뒤에 이어 붙는다)
  [[이름|비었을 때 남길 글|입력 예시]]   한 줄 빈칸"""
import re

from lib import Sec, Mod, e, is_i, only_s, card, prompt
from motion import person, robot

STEPS = ("실습 단계", ["규칙", "1", "2-①", "2-②", "3", "초안"])
NUM = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"
STAGE = {"1": "1. 문제와 목적 정리", "2-①": "2-①. 규정과 선례 확인", "2-②": "2-②. 목표와 해결방안 설계", "3": "3. 실행과 평가 계획",
         "초안": "기획안 초안 작성"}
REQ = {"1": True, "2-①": False, "2-②": True, "3": False, "초안": True}

RULES = """너는 내가 보고서를 준비하는 과정에서 사용하는 보조 도구다.

작업 원칙:
1. 요청 범위 준수: 사용자가 요청한 범위 내에서 충실히 작업하되, 요청에 포함된 하위 항목(예: 분석 + 후보 추천 등)은 생략 없이 함께 수행한다.
2. 단계별 진행: 명시적인 다음 단계나 최종 해결책으로 미리 건너뛰지 않고, 현재 단계의 과제에 집중한다.
3. 사용자 결정권 존중: 문제 정의, 목표, 대안 선택, 최종 계획 등 주요 의사결정은 사용자가 직접 판단할 수 있도록 선택지나 참고 자료 형태로 지원한다.
4. 확정 내용 구분: 사용자가 확정했다고 명시한 사항만 사실 및 전제로 취급한다.
5. 객관성 유지: 사용자의 경험이나 주장을 다룰 때는 '관찰/주장'임을 명확히 구별하여 표현한다.
6. 추정 지양: 확인되지 않은 사실, 수치, 출처는 자의적으로 메우지 않고 미확인 상태임을 밝힌다.
7. 필요시 정보 확인: 작업 수행 중 필수적인 입력이나 명확한 방향 설정이 부족할 경우 핵심 질문을 전달한다.
8. 자료조사 연계: 검색 및 외부 자료 조사는 사용자가 요청하거나 동의한 범위 내에서 수행한다.
9. 누적 정리: 같은 대화의 모든 답변 끝에 지금까지 정리된 사항을 아래 '보고서 준비 현황표'로 이어서 보여준다. '~만 출력해줘'라고 요청한 작업에서도 현황표는 함께 보여주고, 이번 답변에서 새로 채우거나 바뀐 칸은 ★로 표시한다. 내가 확정했다고 말한 내용만 '확정'으로 적는다.

보고서 준비 현황표 (표 하나):
열: 항목 / 내용 요약 / 상태 / 근거·출처
항목: 문제의식, 핵심 문제, 대상·범위, 보고 목적, 규정·선례, 목표, 선택한 대안, 실행·평가 계획, 확인 필요 사항
상태: 확정 · 후보 · 미정 · 미확인 (아직 다루지 않은 항목은 미정)"""
STATUS_ITEMS = ["문제의식", "핵심 문제", "대상·범위", "보고 목적", "규정·선례", "목표", "선택한 대안", "실행·평가 계획", "확인 필요 사항"]
RULE_GROUPS = [("g1", "작업 범위", (1, 2), "요청한 것은 빠짐없이, 다음 단계는 미리 하지 않는다"), ("g2", "결정은 나", (3, 4), "AI는 선택지·자료로 돕고, 확정은 사용자"),
               ("g3", "사실 지키기", (5, 6), "관찰·주장은 구별하고, 미확인은 미확인으로"), ("g4", "질문·조사", (7, 8), "부족하면 핵심 질문, 조사는 요청·동의 범위에서"),
               ("g5", "이어 보기", (9,), "답변마다 현황표로 지금까지를 다시 보여 준다")]

# (번호, 단계, 제목, 결과물, AI가 하지 않는 것, 프롬프트, 앞 안내, 뒤 안내)
TASKS = [
    (1, "1", "문제의식 정리", "분류표 + 핵심 문제 후보 3가지", "해결방안 제안·문제 최종 선택", """아래 내용을 분류하고, 핵심 문제 파악을 도와줘.

[내 경험·관찰·생각]
[[#내 경험·관찰·생각|여기에 입력|예: 안내문이 어려워 민원인이 반복 질문을 한다]]

결과는 다음 표 하나로 작성해줘.
입력 내용 / 사실에 관한 진술·해석·미확인 중 구분 /
제공된 근거 또는 확인 상태

내가 관찰했다고 적은 내용과 자료로 확인된 사실을 구분해줘.
구분된 내용을 바탕으로 내가 가지고 있는 핵심 문제 후보 3가지 추천해줘.""", "", "후보 중 어느 것을 고를지는 내가 정합니다. 고른 문제는 ③에서 한 문장으로 정리합니다."),
    (2, "1", "부족한 정보 질문", "질문 하나", "답이나 판단을 대신 제시", """앞서 정리한 내용을 바탕으로,
핵심 문제와 보고 목적을 정하는 데 필요한 질문 하나만 해줘.

내가 이미 제공한 정보는 다시 묻지 마.
질문에 대한 답이나 판단을 대신 제시하지 말고,
내 답변을 기다려줘.""", "", "필요하면 이 작업을 반복합니다. 질문과 함께 문제 정의까지 작성하게 하지 않습니다."),
    (3, "1", "내가 선택한 핵심 문제 정리", "문제 정의 한 문장", "확인되지 않은 원인·규모 덧붙이기", """내가 선택한 핵심 문제를 한 문장으로 정리해줘.

[내가 선택한 문제]
[[#내가 선택한 문제|여기에 입력]]

[반드시 유지할 대상과 범위]
[[#반드시 유지할 대상과 범위|여기에 입력|예: 처음 신청하는 개인 신청인 · 접수 단계 보완요청만 (심사·수수료 제외)]]

내 선택의 의미와 범위를 유지해줘.
확인되지 않은 원인이나 문제의 규모는 덧붙이지 마.
결과는 문제 정의 한 문장만 출력해줘.""", "", "반드시 유지할 대상과 범위 = AI가 넓히면 안 되는 경계입니다. 누구(문제를 겪는 사람)·어느 단계(절차 중 어디)·뺄 것만 짧게 적습니다. 원인이나 수치는 적지 않습니다."),
    (4, "1", "내가 정한 보고 목적 정리", "보고 목적 한 문장", "적지 않은 결정·추진 방향 추가", """내가 정한 보고 목적을 한 문장으로 정리해줘.

[보고받는 사람]
[[#보고받는 사람|여기에 입력]]

[이번 보고를 통해 결정하거나 확인하려는 것]
[[#이번 보고를 통해 결정하거나 확인하려는 것|여기에 입력]]

내가 적지 않은 결정이나 추진 방향을 추가하지 마.
결과는 보고 목적 한 문장만 출력해줘.""", "", ""),
    (5, "2-①", "관련 규정 조사", "규정 검색 결과표", "우리 업무에 적용되는지 판단", """아래 범위에 해당하는 관련 규정을 공식 원문에서 찾아
검색 결과표로 정리해줘.

[조사할 업무·쟁점]
[[#조사할 업무·쟁점|여기에 입력]]

[적용 대상·지역·확인 기준일]
[[#적용 대상·지역·확인 기준일|여기에 입력]]

표 항목:
규정명 / 법령·행정규칙·지침 등 구분 / 소관·발행기관 /
시행·적용일 / 관련 조문·쪽 / 관련 내용 요약 /
원문 링크 / 원문 확인 여부

원문을 열어 확인하지 못한 자료는 미확인으로 표시해줘.
우리 업무에 적용되는지는 내가 판단하겠다.
결과는 규정 검색 결과표만 출력해줘.""", "", "검색을 요청하는 작업입니다. 공통 규칙 8에 따라 조사는 내가 요청하거나 동의한 범위에서만 합니다."),
    (6, "2-①", "관련 선례 조사", "선례 검색 결과표", "도입 사실과 측정된 성과 섞기", """아래 조건과 관련된 행정선례·다른 기관의 실행 사례를
기관 공식 자료에서 찾아 표로 정리해줘.

[찾고 싶은 사례]
[[#찾고 싶은 사례|여기에 입력]]

[비교에 필요한 조건]
[[#비교에 필요한 조건|기관 유형, 대상, 사업 범위 등을 입력]]

표 항목:
기관·자료명 / 게시·발행일 / 사례의 대상·조건 /
추진 내용 / 자료에서 확인되는 성과 /
확인 위치 / 원문 링크

도입 사실과 측정된 성과를 구분해줘.
성과 수치가 없으면 확인되지 않았다고 적어줘.
결과는 선례 검색 결과표만 출력해줘.""", "", ""),
    (7, "2-①", "내 원문 확인 기록 정리", "사용자 확인 기록표", "내 판단 보충·변경", """아래는 내가 원문을 직접 확인하고 작성한 기록이다.
내 기록을 표로 정리하는 작업만 해줘.

자료명 또는 자료 ID: [[#자료명 또는 자료 ID]]
직접 확인한 조문·쪽·대목: [[#직접 확인한 조문·쪽·대목]]
내 업무에 적용할 내용: [[#내 업무에 적용할 내용]]
적용한다고 판단한 이유: [[#적용한다고 판단한 이유]]
적용할 때의 한계: [[#적용할 때의 한계]]
채택·참고·제외 중 내 선택: [[#채택·참고·제외 중 내 선택]]
추가 확인할 사항: [[#추가 확인할 사항]]

내 판단을 보충하거나 바꾸지 마.
작성하지 않은 항목은 미입력으로 남겨줘.
결과는 사용자 확인 기록표만 출력해줘.""", "이 작업 전에 원문을 직접 읽고 아래 기록을 작성합니다.", ""),
    (8, "2-②", "내가 정한 목표 정리와 대안 추천", "목표 정리표 + 대안 후보 5가지", "정하지 않은 수치·시점 추가, 대안 최종 선택", """내가 정한 목표를 정리하고, 목표 달성에 필요한 대안을 추천해줘.

[변화시키려는 상태]
[[#변화시키려는 상태|여기에 입력]]

[목표 대상·범위]
[[#목표 대상·범위|여기에 입력]]

[내가 정한 목표 수준·달성 시점]
[[#내가 정한 목표 수준·달성 시점|정하지 않았다면 미정이라고 입력]]

먼저 목표 정리표 하나로 정리해줘.
내가 정하지 않은 수치나 달성 시점은 추가하지 마.

그다음 정리한 목표를 달성하는 데 필요한 대안 5가지를 추천해줘.
대안마다 핵심 내용과 목표와의 연결을 한 줄씩 적고,
앞에서 정리한 규정·선례 중 기댈 수 있는 근거가 있으면 함께 적어줘.
확인되지 않은 효과는 단정하지 말고, 어떤 대안을 검토할지는 내가 정하겠다.""", "", "추천받은 5가지 중 검토할 대안을 골라 ⑨에 넣습니다. 내가 따로 생각한 대안을 더해도 됩니다."),
    (9, "2-②", "내 기준에 따른 대안 비교", "대안 비교표", "가중치·점수·순위 만들기, 최종 선택", """내가 제시한 대안을 내가 정한 기준으로 비교해줘.

[검토할 대안]
[[#검토할 대안|여기에 입력]]

[비교 기준]
[[#비교 기준|여기에 입력]]

[비교에 사용할 자료]
[[#비교에 사용할 자료|여기에 입력하거나 첨부]]

결과는 대안 비교표 하나로 작성해줘.
자료로 판단할 수 없는 항목은 판단 근거 부족으로 표시해줘.
내가 정하지 않은 가중치·점수·종합 순위를 만들지 마.
최종 대안은 선택하지 마.""", "", ""),
    (10, "2-②", "내 선택 기록 정리", "선택 기록표", "선택을 정당화할 새 근거·효과 추가", """내가 결정한 내용을 선택 기록표로 정리해줘.

선택한 대안: [[#선택한 대안]]
선택한 이유: [[#선택한 이유]]
선택하지 않은 대안과 그 이유: [[#선택하지 않은 대안과 그 이유]]
선택이 성립하는 조건: [[#선택이 성립하는 조건]]
다시 검토해야 하는 조건: [[#다시 검토해야 하는 조건]]

내가 적은 이유만 사용해줘.
선택을 정당화하기 위한 새로운 근거나 효과를 추가하지 마.
결과는 선택 기록표만 출력해줘.""", "", ""),
    (11, "3", "역할표 작성", "역할표", "정하지 않은 담당·역할 채우기", """아래에서 내가 정한 업무와 담당을 역할표로 정리해줘.

[업무·담당자·협조부서·역할]
[[#업무·담당자·협조부서·역할|여기에 입력]]

표 항목:
업무 / 담당자 / 협조부서 / 담당 범위

정하지 않은 담당이나 역할은 미정으로 표시해줘.
결과는 역할표만 출력해줘.""", "", ""),
    (12, "3", "일정표 작성", "일정표", "일정 임의 추가·조정", """아래에서 내가 정한 과업과 일정을 일정표로 정리해줘.

[과업·시작일·종료일·선행 과업]
[[#과업·시작일·종료일·선행 과업|여기에 입력]]

정하지 않은 날짜는 미정으로 표시하고,
일정을 임의로 추가하거나 조정하지 마.
결과는 일정표만 출력해줘.""", "", ""),
    (13, "3", "예산표 작성", "예산 정리표", "계산 검증 (⑱에서 따로)", """아래 예산 정보를 표로 정리해줘.

[항목·수량·단가·입력된 금액·산출 근거]
[[#항목·수량·단가·입력된 금액·산출 근거|여기에 입력]]

표 항목:
예산 항목 / 수량 / 단가 / 입력된 금액 / 산출 근거

제공된 값을 그대로 옮기고, 없는 값은 미입력으로 표시해줘.
계산 검증은 별도 작업에서 진행하겠다.
결과는 예산 정리표만 출력해줘.""", "", ""),
    (14, "3", "예상 장애요인 정리", "장애요인 정리표", "정하지 않은 대응 채우기", """내가 예상한 장애요인과 대응 내용을 표로 정리해줘.

[예상 장애요인·영향·내가 생각한 대응]
[[#예상 장애요인·영향·내가 생각한 대응|여기에 입력]]

표 항목:
장애요인 / 예상 영향 / 사용자가 제시한 대응

내가 대응을 정하지 않은 항목은 대응 미정으로 표시해줘.
결과는 장애요인 정리표만 출력해줘.""", "", ""),
    (15, "3", "성과 확인 계획 정리", "성과 확인 계획표", "새 지표·목표치 대신 정하기", """내가 정한 성과 확인 방법을 표로 정리해줘.

[성과지표·측정 방법 또는 산식·자료 출처·
측정 시점·담당자·판정 기준]
[[#성과 확인 방법|여기에 입력]]

입력하지 않은 항목은 미정으로 표시해줘.
새로운 지표나 목표치를 대신 정하지 마.
결과는 성과 확인 계획표만 출력해줘.""", "", ""),
    (16, "3", "계획의 누락 항목 점검", "누락 항목표", "누락 내용 대신 작성·계획 수정", """제공한 계획에서 빠진 항목만 찾아줘.

[점검할 계획]
[[#점검할 계획|붙여넣거나 첨부]]

[반드시 포함하기로 한 항목]
[[#반드시 포함하기로 한 항목|여기에 입력]]

결과는 다음 표 하나로 작성해줘.
누락된 항목 / 비어 있는 위치 / 필요한 입력 정보

누락된 내용을 대신 작성하거나 계획을 수정하지 마.""", "", ""),
    (17, "3", "계획 내부의 충돌 점검", "충돌 점검표", "계획 직접 고치기", """제공한 계획 안에서 서로 충돌하는 내용만 찾아줘.

[역할표·일정표·예산표 등 점검할 계획]
[[#점검할 계획|붙여넣거나 첨부]]

결과는 다음 표 하나로 작성해줘.
충돌하는 두 내용 / 각각의 위치 / 충돌하는 이유

확실한 충돌과 추가 확인이 필요한 사항을 구분해줘.
수정 방향은 내가 결정하겠다.
계획을 직접 고치지 마.""", "", ""),
    (18, "3", "예산 계산 점검", "계산 검증표", "사업 필요성·예산 적정성 평가", """아래 예산표의 계산만 검증해줘.

[예산표]
[[#예산표|붙여넣거나 첨부]]

수량×단가, 소계, 합계를 확인해줘.
결과는 다음 표 하나로 작성해줘.
항목 / 입력된 금액 / 계산 결과 / 차이 / 검증 가능 여부

계산에 필요한 값이 없으면 검증 불가로 표시해줘.
사업의 필요성이나 예산의 적정성은 평가하지 마.""", "", ""),
    (19, "3", "성과 측정 방법 점검", "측정 점검표", "지표·목표치 대신 변경", """아래 성과 확인 계획에서
실제로 측정하기 어렵거나 정의가 모호한 부분만 찾아줘.

[성과 확인 계획]
[[#성과 확인 계획|붙여넣거나 첨부]]

결과는 다음 표 하나로 작성해줘.
지표 / 모호하거나 빠진 측정 조건 /
그 상태에서 확인하기 어려운 것

측정 대상·산식·자료 출처·시점·판정 기준을 살펴봐줘.
지표나 목표치를 대신 변경하지 마.""", "", ""),
    (20, "초안", "기획안 초안 작성", "기획안 초안", "새 사실·수치·효과 추가, 내 판단 변경", """아래는 내가 앞 작업에서 확정한 내용이다.
이 내용으로 기획안 초안을 작성하는 작업만 해줘.

[문제 정의 (③)]
[[#문제 정의|여기에 입력]]

[보고 목적 (④)]
[[#보고 목적|여기에 입력]]

[원문 확인 기록 (⑦)]
[[#원문 확인 기록|진행하지 않았다면 없음이라고 입력]]

[목표 정리표 (⑧)]
[[#목표 정리표|여기에 입력]]

[선택 기록표 (⑩)]
[[#선택 기록표|여기에 입력]]

[실행·평가 계획 (⑪~⑮)]
[[#실행·평가 계획|진행하지 않았다면 없음이라고 입력]]

[초안 목차]
[[#초안 목차|여기에 입력|예: 추진 배경 / 현황 및 문제 / 추진 목표 / 추진 방안 / 실행 계획 / 성과 관리]]

내가 제공한 내용만 사용해서 목차 순서대로 작성해줘.
제공되지 않은 사실·수치·출처·효과는 추가하지 말고, 필요한 자리에는 [확인 필요]로 표시해줘.
없음으로 적은 항목에 해당하는 부분은 [자료 없음]으로 표시해줘.
내 판단과 선택을 바꾸거나 보충하지 마.
결과는 기획안 초안 본문만 출력해줘.""", "", "초안은 다음 단계(HWPX 양식과 작성 스킬)에서 ‘확정 기획안’으로 씁니다. 먼저 [확인 필요] 표시를 직접 채우거나 지웁니다."),
]
T = {t[0]: t for t in TASKS}
TOK = re.compile(r"\[\[(#?)([^|\]]+)(?:\|([^|\]]*))?(?:\|([^\]]*))?\]\]")


def n(i):
    return NUM[i - 1]


def mini(fn):
    return f'<svg class="pwho" viewBox="-46 -46 92 92" aria-hidden="true">{fn(0, 0, 44, cls="")}</svg>'


def tpl(key, text):
    """수강생: 빈칸을 채우는 프롬프트, 복사하면 빈칸이 채워진 글이 된다. 강사: 빈칸을 노란 칸으로 보여 준다."""
    if is_i():
        h = TOK.sub(lambda m: f'<span class="blk">{m.group(2)}</span>', e(text))
        return "".join(f'<span class="pp">{x}</span>' for x in h.split("\n\n"))  # 문단이 두 단에 걸쳐 끊기지 않게
    out, k = "", 0
    for ln in text.split("\n"):
        h, pos = "", 0
        for m in TOK.finditer(ln):
            h += e(ln[pos:m.start()])
            multi, label, fb, ph = m.group(1), m.group(2), m.group(3) or "", m.group(4)
            attr = f'data-k="p:{key}:{k}" data-fb="{e(fb)}" aria-label="{e(label)}" placeholder="{e(ph or fb or label)}"'
            h += f'<textarea rows="2" class="bk" {attr}></textarea>' if multi else f'<input type="text" class="bk" {attr}>'
            k, pos = k + 1, m.end()
        h += e(ln[pos:])
        out += f'<span class="ln">{h}</span>'
    return out


def stopsign():
    return ('<svg class="stopsign" viewBox="0 0 100 100" aria-hidden="true"><path d="M30 4h40l26 26v40L70 96H30L4 70V30z" fill="#e8580c"/>'
            '<text x="50" y="60" text-anchor="middle" font-size="27" font-weight="700" fill="#fff">멈춤</text></svg>')


def task_sec(i):
    num, st, title, out, no, text, before, after = T[i]
    meta = (f'<div class="tkh" data-task="t{num:02d}"><span class="pkn">{num}</span><div class="tkm">'
            f'<span class="o">결과물 · {e(out)}</span><span class="n">AI가 하지 않는 것 · {e(no)}</span></div></div>')
    pre = f'<div class="tnote">{e(before)}</div>' if before else ""
    post = f'<p class="tip">{e(after)}</p>' if after else ""
    if is_i():
        side = ('<div class="card stopc">' + stopsign()
                + f'<div class="sti o"><small>결과물</small><b>{e(out)}</b></div>'
                + f'<div class="sti no"><small>AI가 하지 않는 것</small><b>{e(no)}</b></div>'
                + '<div class="sti me"><small>그다음</small><b>내가 확인하고 판단한 뒤 다음 작업</b></div></div>')
        body = (pre + '<div class="i-split wide">'
                + f'<div class="prompt{" two" if text.count(chr(10)) > 24 else ""}"><div class="ph"><span>프롬프트 {n(num)}</span></div><pre>{tpl(f"t{num:02d}", text)}</pre></div>'
                + f'<div class="col">{side}</div></div>' + post)
    else:
        body = (meta + pre
                + f'<div class="tpl"><div class="ph"><span>프롬프트 {n(num)} · 빈칸을 채운 뒤 복사</span><button type="button" class="btn pri" data-tcopy>복사</button></div>'
                + f'<div class="tv">{tpl(f"t{num:02d}", text)}</div></div>' + post)
    tag = "필수" if REQ[st] else "선택"
    return Sec(0, f"{n(num)} {title}", f"{STAGE[st]} · {tag}", body, step=(st,))


def pick(i, g, d=0):
    num, _, title, out = T[i][:4]
    inner = f'<span class="pkn">{num}</span><span><b>{e(title)}</b><small>{e(out)}</small></span>'
    if is_i():
        return f'<div class="pk" style="--i:{d}">{inner}</div>'
    return f'<label class="pk"><input type="checkbox" data-k="pick:t{num:02d}" data-pick="t{num:02d}" data-g="{g}">{inner}</label>'


def pick_tools(g):
    return only_s(f'<div class="pbtns"><button type="button" class="btn" data-pickall="{g}" data-on="1">모두 선택</button>'
                  f'<button type="button" class="btn" data-pickall="{g}" data-on="0">모두 해제</button>'
                  '<small>체크한 작업의 프롬프트만 아래에 나타납니다.</small></div>'
                  f'<p class="pempty" data-empty="{g}">아직 고른 작업이 없습니다. 진행할 작업에 체크하세요.</p>')


def user_step(t):
    return f'<div class="puser">{mini(person)}<span>{e(t)}</span></div>'


# ── 도입 ───────────────────────────────────────
def intro_secs():
    cols =[("규칙", "공통 규칙", True, [], "대화 시작 때 한 번 입력")]
    for st in ("1", "2-①", "2-②", "3", "초안"):
        cols.append((st, STAGE[st].split(". ")[-1], REQ[st], [t[0] for t in TASKS if t[1] == st], ""))
    h = ""
    for ci, (st, name, req, nums, sub) in enumerate(cols):
        if st == "3":
            dots = ('<div class="pnums"><em>작성</em>' + "".join(f'<span style="--j:{j}">{x}</span>' for j, x in enumerate(nums[:5]))
                    + '<em>점검</em>' + "".join(f'<span style="--j:{j + 5}">{x}</span>' for j, x in enumerate(nums[5:])) + "</div>")
        elif nums:
            dots = '<div class="pnums">' + "".join(f'<span style="--j:{j}">{x}</span>' for j, x in enumerate(nums)) + "</div>"
        else:
            dots = f"<small>{e(sub)}</small>"
        tag = "필수" if req else "선택"
        h += (f'<div class="pst{"" if req else " opt"}" style="--i:{ci}"><span class="ptag">{tag}</span>'
              f'<h4>{e(name if st in ("규칙", "초안") else f"{st}. {name}")}</h4>{dots}</div>')
    return [Sec(0, "보고서 작성 프로세스", "실습 방식", f'<div class="pmap" style="--n:{len(cols)}">{h}</div>')]


# ── 모듈 ───────────────────────────────────────
def m0():
    groups = "".join(f'<li class="{g}"><b>{e(t)}</b><span>{"·".join(map(str, ns))}</span><small>{e(s)}</small></li>' for g, t, ns, s in RULE_GROUPS)
    if is_i():
        gmap = {r: g for g, _, ns, _ in RULE_GROUPS for r in ns}
        lines = [l[3:].partition(": ") for l in RULES.split("\n") if l[:1].isdigit()]  # (이름, ": ", 설명)
        rules = "".join(f'<li class="{gmap[k]}" style="--i:{k - 1}"><span class="rn">{k}</span><span><b>{e(n)}</b> {e(d)}</span></li>'
                        for k, (n, _, d) in enumerate(lines, 1))
        body = ('<div class="i-split wide"><div class="col"><p class="rhead">너는 내가 보고서를 준비하는 과정에서 사용하는 보조 도구다.</p>'
                f'<ol class="rules">{rules}</ol></div><div class="col">'
                + card("한 번만 입력", "대화를 시작할 때 맨 처음 입력", "같은 대화창에서 ① 작업부터 이어 갑니다", "새 대화를 열면 다시 입력", dark=True)
                + f'<div class="card"><h4>다섯 묶음</h4><ul class="rgroups">{groups}</ul></div></div></div>')
    else:
        blank = "".join(f"<tr><td>{e(x)}</td><td></td><td><span class=\"st s-0\">미정</span></td><td></td></tr>" for x in STATUS_ITEMS)
        body = (prompt("공통 규칙 · 대화 시작 때 한 번", RULES, example=False)
                + f'<ul class="rgroups">{groups}</ul>'
                + '<h5 class="lab">답변 끝마다 이어지는 보고서 준비 현황표 (처음 모습)</h5>'
                + f'<div class="tw"><table class="stt"><thead><tr><th>항목</th><th>내용 요약</th><th>상태</th><th>근거·출처</th></tr></thead><tbody>{blank}</tbody></table></div>'
                + '<p class="tip">같은 대화창에서 ① 작업부터 이어 갑니다. 작업을 할 때마다 표의 빈칸이 채워지고, 바뀐 칸에는 ★가 붙습니다. 새 대화를 열면 공통 규칙을 다시 입력합니다.</p>')
    secs = [Sec(0, "공통 규칙: 대화 시작 때 한 번", "공통 규칙 · 필수", body, step=("규칙",))]
    if is_i():
        secs.append(status_sec())
    return Mod("0", "공통 규칙 입력", "", "", "AI 작업 원칙 설정", "", "필수 · 대화를 시작할 때 한 번 입력합니다.", secs)


def status_sec():
    """강사: 한 채팅에서 현황표가 ①→③→④를 지나며 채워지는 모습 (클릭마다 한 단계)."""
    # 항목: (단계별 (내용, 상태, 바뀜) — 단계 0: ① 뒤, 1: ③ 뒤, 2: ④ 뒤)
    obs = ("안내문이 어려워 반복 질문 (내 관찰)", "미확인")
    rows = {
        "문제의식": [obs + (1,), obs + (0,), obs + (0,)],
        "핵심 문제": [("후보 3가지", "후보", 1), ("신청서 작성 안내 탓 보완요청 반복", "확정", 1), ("신청서 작성 안내 탓 보완요청 반복", "확정", 0)],
        "대상·범위": [("", "미정", 0), ("개인 첫 신청 · 접수 단계", "확정", 1), ("개인 첫 신청 · 접수 단계", "확정", 0)],
        "보고 목적": [("", "미정", 0), ("", "미정", 0), ("과장 보고 · 시범운영 여부 결정", "확정", 1)],
        "확인 필요 사항": [("반복 질문 건수 자료 없음", "미확인", 1), ("반복 질문 건수 자료 없음", "미확인", 0), ("반복 질문 건수 자료 없음", "미확인", 0)],
    }
    code = {"확정": 3, "후보": 1, "미확인": 2, "미정": 0}
    body = ""
    for item in STATUS_ITEMS:
        vals = rows.get(item, [("", "미정", 0)] * 3)
        cells = ["", "", ""]
        for k, (txt, st, new) in enumerate(vals):
            star = '<i class="star">★</i>' if new else ""
            cells[0] += f'<span class="v v{k}">{star}{e(txt)}</span>'
            cells[1] += f'<span class="v v{k}"><span class="st s-{code[st]}">{e(st)}</span></span>'
        body += f"<tr><td>{e(item)}</td><td>{cells[0]}</td><td>{cells[1]}</td></tr>"
    steps = "".join(f'<li class="w{k}">{e(t)}</li>' for k, t in enumerate(("① 문제의식 정리 뒤", "③ 핵심 문제 정리 뒤", "④ 보고 목적 정리 뒤")))
    html = (f'<div class="i-split wide"><div class="tw"><table class="stt live"><thead><tr><th>항목</th><th>내용 요약</th><th>상태</th></tr></thead><tbody>{body}</tbody></table></div>'
            f'<div class="col"><ol class="stw">{steps}</ol>'
            + card("왜 현황표인가", "한 채팅에서 이어 가므로, 지금까지 무엇이 확정됐는지 매번 눈으로 확인", "★ = 이번 답변에서 바뀐 칸", "확정은 내가 말한 것만", dark=True)
            + '</div></div><p class="muted">가상 예시 · 실제 표에는 ‘근거·출처’ 열도 함께 나옵니다.</p>')
    return Sec(0, "한 채팅에서 이어지는 보고서 준비 현황표", "공통 규칙 · 필수", html, role="i", steps=2, step=("규칙",))


def example_sec():
    rows = [("1", "정리", "‘원인에 대한 해석’으로 분류 + 문제 후보 3가지", "멈춤 · 내가 고름"),
            ("2", "질문", "“그렇게 판단한 사례나 자료가 있습니까?”", "멈춤 · 내 답 기다림"),
            ("3", "정리", "내가 고른 문제만 한 문장으로", "멈춤")]
    r = "".join(f'<div class="pexr" style="--i:{i}"><span class="pkn">{a}</span><b>{e(b)}</b><div class="pexo">{mini(robot)}<span>{e(c)}</span></div>'
                f'<span class="pstop">{e(d)}</span></div>' for i, (a, b, c, d) in enumerate(rows))
    body = (f'<div class="pex"><div class="pexin">{mini(person)}<span>내 입력: “안내문이 어려워서 민원인이 반복 질문하는 것 같다”</span></div>{r}</div>'
            '<p class="pnote">AI는 후보만 내고, 문제를 고르고 확정하는 것은 내가 합니다. ②에서 문제 정의까지 쓰게 하지 않습니다.</p>')
    return Sec(0, "예시: 한 작업씩 멈추는 모습", f'{STAGE["1"]} · 필수', body, step=("1",))


def m1():
    return Mod("1", "문제와 목적 정리", "", "", "문제 정의 한 문장, 보고 목적 한 문장", "", "필수 · 네 가지 작업 ①~④로 나눕니다.",
               [example_sec()] + [task_sec(i) for i in (1, 2, 3, 4)])


def m21():
    def col(lab, inner):
        return f'<div class="pcol"><span class="plab">{lab}</span><div class="pcb">{inner}</div></div>'
    arr = col("", '<span class="parr">→</span>')
    proc = ('<div class="pproc">' + col("AI 검색", pick(5, "2-①", 0) + pick(6, "2-①", 1)) + arr
            + col("내가 직접", user_step("원문을 직접 읽고 확인 기록 작성")) + arr
            + col("AI 정리", pick(7, "2-①", 2)) + "</div>" + pick_tools("2-①"))
    first = Sec(0, "2-① 진행 순서: 필요한 작업 고르기", f'{STAGE["2-①"]} · 선택', proc, step=("2-①",))
    return Mod("2-1", "규정과 선례 확인", "", "", "규정·선례 검색 결과표, 원문 확인 기록표", "",
               "선택 · 진행 순서를 보고 필요한 작업(⑤~⑦)만 골라 진행합니다.", [first] + [task_sec(i) for i in (5, 6, 7)])


def m22():
    flow = "".join(f'<div class="pk" style="--i:{d}"><span class="pkn">{i}</span><span><b>{e(T[i][2])}</b><small>{e(T[i][3])}</small></span></div>'
                   + ('<span class="parr">→</span>' if d < 2 else "") for d, i in enumerate((8, 9, 10)))
    first = Sec(0, "2-② 진행 순서", f'{STAGE["2-②"]} · 필수', f'<div class="pline">{flow}</div>'
                '<p class="pnote">AI는 목표 정리, 대안 후보 추천, 비교표를 만듭니다. 검토할 대안·비교 기준·최종 선택은 내가 정합니다.</p>', step=("2-②",))
    return Mod("2-2", "목표와 해결방안 설계", "", "", "목표 정리표, 대안 비교표, 선택 기록표", "",
               "필수 · 세 가지 작업 ⑧~⑩으로 나눕니다.", [first] + [task_sec(i) for i in (8, 9, 10)])


def m3():
    mk = "".join(pick(i, "3", d) for d, i in enumerate((11, 12, 13, 14, 15)))
    ck = "".join(pick(i, "3", d + 5) for d, i in enumerate((16, 17, 18, 19)))
    proc = (f'<div class="pproc3"><span class="plab">표 만들기</span><div class="prow n5">{mk}</div>'
            f'<div class="pmid"><span class="parr">↓</span>{user_step("만든 표를 모아 ‘점검할 계획’으로 붙여 넣기")}<span class="parr">↓</span></div>'
            f'<span class="plab">점검하기</span><div class="prow n4">{ck}</div>'
            '<p class="pnote">짝: ⑬ 예산표 → ⑱ 계산 점검, ⑮ 성과 확인 계획 → ⑲ 측정 방법 점검. ⑯ 누락·⑰ 충돌은 계획 전체를 봅니다.</p></div>'
            + pick_tools("3"))
    first = Sec(0, "3 진행 순서: 만들기와 점검을 나눠 고르기", f'{STAGE["3"]} · 선택', proc, step=("3",))
    return Mod("3", "실행과 평가 계획", "", "", "역할·일정·예산·장애요인·성과 확인 계획표와 점검표", "",
               "선택 · 표를 만드는 작업(⑪~⑮)과 점검하는 작업(⑯~⑲)을 나눠, 필요한 것만 골라 진행합니다.",
               [first] + [task_sec(i) for i in range(11, 20)])


def m_draft():
    return Mod("초안", "기획안 초안 작성", "", "", "기획안 초안", "",
               "필수 · 앞에서 확정한 결과만 모아 초안 하나를 씁니다 (⑳).", [task_sec(20)])


def modules():
    return [m0(), m1(), m21(), m22(), m3(), m_draft()]


JS = r"""
(function () {
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var tt;
  function toast(t) { var el = document.getElementById("toast"); el.textContent = t; el.classList.add("on"); clearTimeout(tt); tt = setTimeout(function () { el.classList.remove("on"); }, 1800); }
  function copy(text) {
    function ok() { toast("프롬프트를 복사했습니다"); }
    function fb() { var t = document.createElement("textarea"); t.value = text; document.body.appendChild(t); t.select(); try { document.execCommand("copy"); ok(); } catch (e) { toast("복사하지 못했습니다"); } t.remove(); }
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(ok, fb); else fb();
  }
  /* 빈칸을 채운 글. 비운 칸은 원래 안내 문구(예: 여기에 입력)를 남긴다 */
  function text(tv) {
    return $$(".ln", tv).map(function (ln) {
      var s = "";
      [].forEach.call(ln.childNodes, function (c) {
        if (c.nodeType === 3) s += c.nodeValue;
        else if (c.matches("input,textarea")) s += c.value.trim() || c.getAttribute("data-fb");
        else s += c.textContent;
      });
      return s.replace(/\s+$/, "");
    }).join("\n").trim();
  }
  /* 선택 단계: 체크한 작업만 본문과 목차에 보인다 */
  function apply() {
    $$("[data-pick]").forEach(function (c) {
      var h = document.querySelector('.tkh[data-task="' + c.getAttribute("data-pick") + '"]');
      if (!h) return;
      var sec = h.closest(".sec"), a = document.querySelector('nav a[href="#' + sec.id + '"]');
      sec.hidden = !c.checked;
      if (a) a.hidden = !c.checked;
    });
    $$("[data-empty]").forEach(function (p) {
      p.hidden = $$('[data-pick][data-g="' + p.getAttribute("data-empty") + '"]').some(function (c) { return c.checked; });
    });
  }
  document.addEventListener("click", function (ev) {
    var b = ev.target.closest && ev.target.closest("button");
    if (!b) return;
    if (b.hasAttribute("data-tcopy")) copy(text(b.closest(".tpl").querySelector(".tv")));
    if (b.hasAttribute("data-pickall")) {
      var on = b.getAttribute("data-on") === "1";
      $$('[data-pick][data-g="' + b.getAttribute("data-pickall") + '"]').forEach(function (c) {
        if (c.checked !== on) { c.checked = on; c.dispatchEvent(new Event("change")); }
      });
      apply();
    }
    if (b.id === "clearAll") apply();
  });
  document.addEventListener("change", function (ev) { if (ev.target.hasAttribute && ev.target.hasAttribute("data-pick")) apply(); });
  apply();
})();
"""

CSS = """
.sec[hidden],nav a[hidden],.pempty[hidden]{display:none!important}
.pwho{width:36px;height:36px;flex:none}
.pkn{width:28px;height:28px;border-radius:50%;background:var(--blue);color:#fff;display:grid;place-items:center;font-weight:700;font-size:15px;flex:none}
.pmap{display:grid;grid-template-columns:repeat(var(--n),minmax(0,1fr));gap:22px}
.pst{position:relative;border:2px solid var(--blue);border-radius:14px;padding:14px;background:#fff;display:flex;flex-direction:column;gap:8px;min-width:0}
.pst.opt{border-style:dashed;border-color:#9ea1aa}.pst+.pst:before{content:"→";position:absolute;left:-19px;top:40%;color:var(--soft);font-size:18px}
.ptag{align-self:flex-start;background:var(--blue);color:#fff;border-radius:99px;padding:2px 10px;font-size:12.5px;font-weight:600}.opt .ptag{background:#6f7077}
.pst h4{font-size:16px;line-height:1.35}.pst small{color:var(--mid);font-size:13px}
.pnums{display:flex;flex-wrap:wrap;gap:4px}.pnums span{width:30px;height:30px;border-radius:50%;background:#e6f0fc;color:var(--blue);display:grid;place-items:center;font-size:15px;font-weight:700}
.opt .pnums span{background:#f2f3f5;color:var(--mid)}.pnums em{width:100%;font-style:normal;font-size:12px;color:var(--soft);margin-top:2px}
.pnote{font-size:14.5px;color:var(--mid)}.pnote b{color:var(--ink)}
.rgroups{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.rgroups li{border-left:5px solid var(--g);background:#fff;border-radius:8px;padding:8px 12px;border-top:1px solid var(--line);border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.rgroups b{font-size:14.5px}.rgroups span{margin-left:8px;color:var(--g);font-weight:700;font-size:13px}.rgroups small{display:block;color:var(--mid);font-size:13px}
.g1{--g:#0866d6}.g2{--g:#26262a}.g3{--g:#f26a10}.g4{--g:#12a37a}.g5{--g:#7b5cd6}
.stt td,.stt th{font-size:14px}.stt td:first-child{font-weight:600;white-space:nowrap}
.st{display:inline-block;border-radius:99px;padding:1px 10px;font-size:12.5px;font-weight:700;white-space:nowrap}
.st.s-0{background:#f2f3f5;color:var(--soft)}.st.s-1{background:#fff3c4;color:#8a6a00}.st.s-2{background:#fdeee3;color:#b44a05}.st.s-3{background:#e6f0fc;color:var(--blue)}
.pproc{display:grid;grid-template-columns:minmax(0,1fr) 26px minmax(0,.8fr) 26px minmax(0,1fr);align-items:stretch;gap:8px}
.pcol{display:flex;flex-direction:column;gap:8px}.pcb{flex:1;display:flex;flex-direction:column;justify-content:center;gap:8px}.plab{font-size:13.5px;font-weight:700;color:var(--blue);min-height:1.5em}
.pproc3{display:flex;flex-direction:column;gap:8px}.prow{display:grid;gap:8px}.prow.n5{grid-template-columns:repeat(5,minmax(0,1fr))}.prow.n4{grid-template-columns:repeat(4,minmax(0,1fr))}
.pmid{display:flex;align-items:center;justify-content:center;gap:12px}
.pk{display:flex;gap:10px;align-items:flex-start;border:2px solid var(--line);border-radius:12px;padding:10px 12px;background:#fff;min-width:0}
label.pk{cursor:pointer}.pk:has(input:checked){border-color:var(--blue);background:#f3f8fe}
.pk input{width:18px;height:18px;accent-color:var(--blue);margin-top:5px;flex:none}.pk b{display:block;font-size:15px;line-height:1.35}.pk small{display:block;font-size:12.5px;color:var(--mid)}
.puser{display:flex;gap:10px;align-items:center;border:2px dashed #e8580c;border-radius:12px;padding:10px 12px;background:#fff8f2;font-size:14.5px;font-weight:600;color:#b44a05}
.parr{text-align:center;color:var(--soft);font-size:22px}
.pline{display:grid;grid-template-columns:minmax(0,1fr) 26px minmax(0,1fr) 26px minmax(0,1fr);align-items:center;gap:8px}.pline .pk b{white-space:nowrap}
.pbtns{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.pbtns small{color:var(--mid);font-size:13.5px}
.pempty{border:1px dashed var(--soft);border-radius:10px;padding:10px 14px;color:var(--mid);font-size:14px}
.tkh{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.tkm{display:flex;gap:6px;flex-wrap:wrap}
.tkm span{border-radius:99px;padding:4px 12px;font-size:13px;font-weight:600}.tkm .o{background:#e6f0fc;color:var(--blue)}.tkm .n{background:#fdeee3;color:#b44a05}
.tnote{border-left:4px solid #e8580c;background:#fff8f2;padding:10px 14px;border-radius:0 10px 10px 0;font-size:14.5px;font-weight:600}
.tpl{border:1px solid #bcd6f3;background:#f7fbff;border-radius:12px;overflow:hidden}.tpl .ph{padding:10px 14px;color:var(--blue);font-weight:600;font-size:13.5px}
.tv{padding:2px 16px 16px;font-size:15px;line-height:1.75}.ln{display:block;min-height:1.75em;white-space:pre-wrap}
.tv textarea.bk{width:100%}.tv input.bk{width:min(36ch,100%)}
.pex{display:flex;flex-direction:column;gap:10px}.pexin{display:flex;gap:10px;align-items:center;background:var(--dark);color:#fff;border-radius:12px;padding:10px 14px;font-size:15px}
.pexr{display:grid;grid-template-columns:28px 44px minmax(0,1fr) auto;gap:10px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:12px;padding:8px 12px}
.pexr>b{font-size:14.5px}.pexo{display:flex;gap:10px;align-items:center;font-size:15px}
.pstop{color:#e8580c;border:2px solid #e8580c;border-radius:99px;padding:3px 10px;font-size:12.5px;font-weight:700;white-space:nowrap}
@media(max-width:680px){.pline .pk b{white-space:normal}.pmap,.pproc,.pline,.prow.n5,.prow.n4,.rgroups{grid-template-columns:minmax(0,1fr)}.pst+.pst:before{content:"↓";left:50%;top:-20px}.pproc .parr,.pline .parr{transform:rotate(90deg)}.pexr{grid-template-columns:28px minmax(0,1fr)}.pexr>b,.pstop{display:none}}
"""

DECK_CSS = """
.slide .pwho{width:44px;height:44px}.slide .pkn{width:36px;height:36px;font-size:18px}
.slide .pmap{gap:28px}.slide .pst{padding:18px;gap:12px}.slide .pst h4{font-size:20px}.slide .pst small{font-size:16px}.slide .ptag{font-size:14px}
.slide .pnums span{width:38px;height:38px;font-size:18px}.slide .pnums em{font-size:14px}.slide .pst+.pst:before{left:-23px;font-size:22px}
.active .pst{animation:rise .45s ease both;animation-delay:calc(var(--i)*.22s)}.active .pnums span{animation:pop .35s ease both;animation-delay:calc(.25s + var(--i)*.22s + var(--j)*.05s)}
.slide .pnote{font-size:17px}
.rhead{font-size:17px;color:var(--mid)}.rules{display:grid;gap:7px}
.rules li{display:grid;grid-template-columns:30px minmax(0,1fr);gap:12px;align-items:center;background:#fff;border:1px solid var(--line);border-left:6px solid var(--g);border-radius:8px;padding:7px 12px;font-size:17.5px}
.rn{width:28px;height:28px;border-radius:50%;background:var(--g);color:#fff;display:grid;place-items:center;font-size:14px;font-weight:700}
.rules b{color:var(--g);font-weight:700}.active .rules li{animation:slidein .35s ease both;animation-delay:calc(.15s + var(--i)*.12s)}
.slide .rgroups{grid-template-columns:1fr}.slide .rgroups b{font-size:16.5px}.slide .rgroups small{font-size:14.5px}
.slide .pk{padding:14px 16px}.slide .pk b{font-size:18.5px}.slide .pk small{font-size:15px}.slide .plab{font-size:16px}.slide .puser{font-size:18px;padding:14px 16px}
.active .pk{animation:rise .4s ease both;animation-delay:calc(.1s + var(--i)*.15s)}.active .puser{animation:pop .45s ease both .9s}
.slide .pproc{grid-template-columns:minmax(0,1fr) 34px minmax(0,.85fr) 34px minmax(0,1fr)}.slide .pline{grid-template-columns:auto 34px auto 34px auto;justify-content:center}
.slide .tnote{font-size:17px}
.slide .stt td,.slide .stt th{font-size:16px;padding:8px 12px;height:auto}.slide .st{font-size:14px}
.stt.live .v{display:none}.stt.live .v0{display:inline}.slide[data-step="1"] .stt.live .v0,.slide[data-step="2"] .stt.live .v0{display:none}
.slide[data-step="1"] .stt.live .v1{display:inline}.slide[data-step="2"] .stt.live .v2{display:inline}
.stt .star{font-style:normal;color:#e8582a;margin-right:6px}.active .stt .star{animation:pop .5s ease both .2s}
.stw{display:grid;gap:8px}.stw li{border:2px solid var(--line);border-radius:10px;padding:10px 14px;font-size:17px;font-weight:600;color:var(--soft);transition:all .3s}
.slide:not([data-step]) .stw .w0,.slide[data-step="0"] .stw .w0,.slide[data-step="1"] .stw .w1,.slide[data-step="2"] .stw .w2{border-color:var(--blue);color:var(--blue);background:#f3f8fe}
.slide .prompt.two pre{column-count:2;column-gap:30px}
.slide .prompt .pp{display:block;break-inside:avoid}.slide .prompt .pp+.pp{margin-top:1.6em}
.stopc{display:flex;flex-direction:column;gap:14px}.stopsign{width:76px;height:76px}.active .stopsign{animation:pop .5s ease both .5s}
.sti small{display:block;font-size:14.5px;color:var(--soft)}.sti b{font-size:20px;line-height:1.35}.sti.o b{color:var(--blue)}.sti.no b{color:#b44a05}
.active .sti{animation:rise .4s ease both}.active .sti.o{animation-delay:.7s}.active .sti.no{animation-delay:.9s}.active .sti.me{animation-delay:1.1s}
.slide .prompt pre .blk{color:#1d1d20;font-weight:600}
.slide .pexin{font-size:19px;padding:14px 18px}.slide .pexr{grid-template-columns:36px 60px minmax(0,1fr) auto;padding:12px 16px;gap:14px}.slide .pexr>b{font-size:18px}.slide .pexo{font-size:19px}.slide .pstop{font-size:15px;padding:4px 12px}
.active .pexin{animation:rise .4s ease both}.active .pexr{animation:slidein .4s ease both;animation-delay:calc(.5s + var(--i)*.5s)}.active .pstop{animation:pop .4s ease both;animation-delay:calc(.8s + var(--i)*.5s)}
"""
