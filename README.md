# 추측의 교실 · Lakatos

고등학교 미적분Ⅰ 수업에서 추측·증명 검토·반례·추측 개선을 함께 기록하는 수업 도구입니다.

수업 화면: https://dkim-23.github.io/lakatos/

## 사용

1. 학년·반·교시와 학생이 제시한 추측을 입력합니다.
2. ‘증명해 보기’로 단계별 증명을 표시합니다.
3. 학생들의 반례와 개선된 추측을 입력해 토의 과정에 추가합니다.
4. 마지막에 ‘오류와 수정 방향 함께 보기’로 비교합니다.
5. 수업 기록을 HTML·LaTeX·PDF로 저장합니다. 날짜·교시·학교·학년·반도 포함됩니다.

교사·학생 화면 구분 없이 선생님의 컴퓨터 화면을 함께 보는 방식입니다. 다른 기기 간 자동 동기화는 없습니다. 수업 상태는 현재 브라우저에만 저장되며 GitHub에 업로드되지 않습니다.

## AI 연결

기본 수업 사례 5개는 키 없이 작동합니다. 그 외 추측은 Cloudflare Worker가 필요합니다. 화면의 API 키 입력 기능은 제거했습니다.

- `cloudflare/worker.js`: AI 요청을 처리하는 Worker 코드. 허용된 출처는 `https://dkim-23.github.io`로 설정했습니다.
- `wrangler.jsonc`, `package.json`: 이 저장소를 Cloudflare Workers에 연결하는 배포 설정입니다. 저장소 루트에서 빌드 명령 없이 `npx wrangler deploy`로 배포합니다.
- Cloudflare Worker의 Settings → Variables and Secrets에 `GEMINI_API_KEY`를 **Secret**으로 등록합니다. GitHub에는 API 키를 저장하지 않습니다.
- `lakatos-config.js`의 `workerUrl`에 실제 Worker 주소를 입력하고 커밋합니다. `/proof`는 붙이지 않습니다. 현재 빈 값이므로 자유 추측 AI 생성은 연결 완료 전까지 사용할 수 없습니다.

설정이 끝나면 수업 링크를 열어 키 입력 없이 사용합니다. 기본 예시를 제외한 추측이 Gemini API로 전송됩니다. 무료 사용 가능 여부와 사용량 한도는 계정에서 확인합니다. 실제 API 키로 호출하거나 Cloudflare에 배포한 상태는 아닙니다.

## 저장과 수식

수식은 `\(f'(a)=0\)` 또는 `\[\lim_{h\to0}\frac{f(a+h)-f(a)}{h}\]`처럼 입력합니다. KaTeX와 고운돋움·주아 글꼴은 CDN을 사용합니다.

HTML 저장본은 브라우저에서 열 수 있습니다. LaTeX 저장본은 kotex를 지원하는 XeLaTeX 환경에서 컴파일합니다. PDF는 브라우저 인쇄 창에서 저장합니다. 비교 해설은 ‘함께 보기’를 켠 경우 저장본에 포함됩니다.

## 개발 확인

```sh
node tests/test_worker.mjs
```

프록시 요청·응답, 출처 제한, 입력 길이, 키 누락 및 사용량 오류를 모의 테스트합니다. `server.py`는 과거 로컬 서버 방식의 소스이며 현재 수업 화면은 사용하지 않습니다.
