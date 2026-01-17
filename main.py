import os
from dotenv import load_dotenv
from github_api import GitHubAnalyzer
from analyzer import StatsAnalyzer
from github import Github, InputFileContent

# 0. 환경 변수 로드
load_dotenv()

TOKEN = os.getenv('GH_TOKEN')
USERNAME = os.getenv('GH_USERNAME')
GIST_ID = os.getenv('GIST_ID')


def update_gist(content):
    """분석된 텍스트를 실제 GitHub Gist에 업데이트합니다."""
    if not GIST_ID or not TOKEN:
        print("GIST_ID 또는 TOKEN이 설정되지 않아 Gist 업데이트를 건너뜁니다.")
        return

    # 최신 PyGithub 버전의 권장 방식으로 수정 (DeprecationWarning 해결)
    from github import Auth
    auth = Auth.Token(TOKEN)
    g = Github(auth=auth)

    try:
        gist = g.get_gist(GIST_ID)
        filename = list(gist.files.keys())[0]  # 기존 Gist의 첫 번째 파일명 유지

        # InputFileContent 객체를 사용하여 내용 업데이트
        gist.edit(
            description="Weekly Development Reflection",
            files={filename: InputFileContent(content=content)}
        )
        print(f"✅ Gist 업데이트 완료! (ID: {GIST_ID})")
    except Exception as e:
        print(f"❌ Gist 업데이트 중 오류 발생: {e}")


def main():
    # 1. 데이터 가져오기 (GitHub API)
    print(f"🔍 {USERNAME}님의 지난주 활동을 분석 중...")
    api = GitHubAnalyzer(TOKEN)
    exts, dates = api.get_last_week_data(USERNAME)
    streak = api.calculate_streak(dates)

    # 2. 분석하기 (Stats Analyzer)
    analyzer = StatsAnalyzer(mapping_path='mappings.json')
    stats = analyzer.analyze_categories(exts)

    # 3. 텍스트 생성 및 시각화
    # 가장 많이 쓴 확장자에서 '.' 제거 후 대문자로 표시 (ex: .java -> JAVA)
    top_lang_raw = max(set(exts), key=exts.count) if exts else "N/A"
    top_lang = top_lang_raw.replace('.', '').upper()

    final_text = analyzer.format_gist_text(stats, streak, top_lang)

    # 4. 결과 출력 및 Gist 업데이트
    print("\n" + "=" * 30)
    print(final_text)
    print("=" * 30 + "\n")

    update_gist(final_text)


if __name__ == "__main__":
    main()