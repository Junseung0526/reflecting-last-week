import os
from dotenv import load_dotenv
from github_api import GitHubAnalyzer
from analyzer import StatsAnalyzer
from github import Github, InputFileContent

load_dotenv()

TOKEN = os.getenv('GH_TOKEN')
USERNAME = os.getenv('GH_USERNAME')
GIST_ID = os.getenv('GIST_ID')


def update_gist(content):
    """분석된 텍스트를 실제 GitHub Gist에 업데이트합니다."""
    if not GIST_ID or not TOKEN:
        print("GIST_ID 또는 TOKEN이 설정되지 않아 Gist 업데이트를 건너뜁니다.")
        return

    from github import Auth
    auth = Auth.Token(TOKEN)
    g = Github(auth=auth)

    try:
        gist = g.get_gist(GIST_ID)
        filename = list(gist.files.keys())[0]

        gist.edit(
            description="Weekly Development Reflection",
            files={filename: InputFileContent(content=content)}
        )
        print(f"Gist 업데이트 완료 (ID: {GIST_ID})")
    except Exception as e:
        print(f"Gist 업데이트 중 오류 발생: {e}")


def main():
    print(f"🔍 {USERNAME}님의 최근 30일 활동을 분석 중...")
    api = GitHubAnalyzer(TOKEN)
    exts, dates = api.get_last_week_data(USERNAME)
    streak = api.calculate_streak(dates)

    analyzer = StatsAnalyzer(mapping_path='mappings.json')
    stats = analyzer.analyze_categories(exts)

    top_lang_raw = max(set(exts), key=exts.count) if exts else "N/A"
    top_lang = top_lang_raw.replace('.', '').upper()

    final_text = analyzer.format_gist_text(stats, streak, top_lang)

    print("\n" + "=" * 30)
    print(final_text)
    print("=" * 30 + "\n")

    update_gist(final_text)


if __name__ == "__main__":
    main()