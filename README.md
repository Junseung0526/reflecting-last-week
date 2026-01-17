# Reflecting Last Week

지난 7일간의 GitHub 활동을 분석하여 개발 현황을 GitHub Gist에 자동으로 업데이트하는 프로젝트입니다.

## 주요 기능

- **최근 7일 활동 분석**: 지난 일주일간 작업한 파일 확장자 및 카테고리별 통계 분석
- **커밋 스트릭 추적**: 연속 커밋 일수 자동 계산
- **주 사용 언어 감지**: 가장 많이 작업한 프로그래밍 언어 표시
- **자동화**: GitHub Actions를 통해 매일 자동 업데이트
- **Gist 연동**: 분석 결과를 GitHub Gist에 깔끔하게 표시

## GitHub Actions 설정 방법

### 1. 저장소 준비

이 저장소를 본인의 GitHub 계정으로 Fork 또는 Clone합니다.

```bash
git clone https://github.com/YOUR_USERNAME/reflecting-last-week.git
cd reflecting-last-week
```

### 2. GitHub Personal Access Token 생성

1. GitHub 설정 > Developer settings > Personal access tokens > Tokens (classic) 이동
2. "Generate new token (classic)" 클릭
3. 다음 권한 선택:
   - `repo` (전체)
   - `gist` (전체)
   - `read:user`
4. 생성된 토큰을 안전한 곳에 복사

### 3. Gist 생성

1. [GitHub Gist](https://gist.github.com/) 접속
2. 새 Gist 생성 (파일명과 내용은 자유롭게 작성)
3. URL에서 Gist ID 복사
   - 예: `https://gist.github.com/username/abc123...` → `abc123...`

### 4. Repository Secrets 설정

저장소의 Settings > Secrets and variables > Actions로 이동하여 다음 3개의 secrets를 추가합니다:

| Name | Description | Example |
|------|-------------|---------|
| `GH_TOKEN` | 2단계에서 생성한 Personal Access Token | `ghp_xxxxxxxxxxxx` |
| `GH_USERNAME` | 본인의 GitHub username | `your-username` |
| `GIST_ID` | 3단계에서 생성한 Gist ID | `abc123def456...` |

### 5. GitHub Actions 활성화

1. 저장소의 **Actions** 탭으로 이동
2. 워크플로우를 활성화 (필요한 경우)
3. "Update Reflecting Last Week Gist" 워크플로우가 표시되어야 합니다

### 6. 완료!

이제 매일 한국 시간 기준 오전 0시 10분에 자동으로 실행됩니다.

## 수동 실행

자동 실행을 기다리지 않고 즉시 실행하려면:

1. 저장소의 **Actions** 탭 이동
2. 좌측에서 "Update Reflecting Last Week Gist" 워크플로우 선택
3. 우측 상단 **Run workflow** 버튼 클릭
4. **Run workflow** 확인

## 로컬 테스트

로컬 환경에서 테스트하려면:

1. `.env` 파일 생성:

```bash
GH_TOKEN=your_github_token
GH_USERNAME=your_username
GIST_ID=your_gist_id
```

2. 의존성 설치:

```bash
pip install PyGithub python-dotenv
```

3. 실행:

```bash
python main.py
```

## 📝 커스터마이징

### 카테고리 변경

`mappings.json` 파일을 수정하여 파일 확장자별 카테고리를 변경할 수 있습니다.

```json
{
  "Frontend": [".js", ".jsx", ".tsx", ".vue", ".html", ".css"],
  "Backend": [".py", ".java", ".go", ".rb"],
  "DevOps": [".yml", ".yaml", ".dockerfile"]
}
```

### 실행 시간 변경

`.github/workflows/schedule.yml` 파일의 cron 표현식을 수정합니다:

```yaml
on:
  schedule:
    # 매일 한국 시간 기준 오전 0시 10분 (UTC 15:10)
    - cron: '10 15 * * *'
```

## 기술 스택

- Python 3.10
- [PyGithub](https://github.com/PyGithub/PyGithub) - GitHub API 클라이언트
- GitHub Actions - 자동화 워크플로우

## 라이선스

MIT License