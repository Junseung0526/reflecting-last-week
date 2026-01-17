import datetime
import os
from github import Github
from dotenv import load_dotenv

load_dotenv()


class GitHubAnalyzer:
    def __init__(self, token):
        # 최신 PyGithub 권장 방식 적용
        from github import Auth
        auth = Auth.Token(token)
        self.g = Github(auth=auth)

    def get_last_week_data(self, username):
        """
        확장자 통계(최근 7일)와 스트릭 계산을 위한 날짜 데이터(전체)를 가져옵니다.
        """
        user = self.g.get_user(username)
        seven_days_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)

        extensions = []
        commit_dates = set()

        events = user.get_events()

        print("데이터 수집 중... 잠시만 기다려주세요.")
        for event in events:
            if event.type == "PushEvent":
                commit_dates.add(event.created_at.date())

                if event.created_at >= seven_days_ago:
                    repo = event.repo
                    for commit_payload in event.payload.get('commits', []):
                        try:
                            commit = repo.get_commit(commit_payload['sha'])
                            for file in commit.files:
                                filename = file.filename
                                if '.' in filename:
                                    ext = "." + filename.split('.')[-1].lower()
                                    extensions.append(ext)
                                else:
                                    extensions.append(filename)
                        except Exception:
                            continue


        return extensions, commit_dates

    def calculate_streak(self, commit_dates):
        """
        연속 커밋 일수(Streak)를 계산합니다.
        """
        if not commit_dates:
            return 0

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)

        if today not in commit_dates and yesterday not in commit_dates:
            return 0

        streak = 0
        current_check = today if today in commit_dates else yesterday

        while current_check in commit_dates:
            streak += 1
            current_check -= datetime.timedelta(days=1)

        return streak


# 테스트 코드
if __name__ == "__main__":
    TOKEN = os.getenv('GH_TOKEN')
    USERNAME = os.getenv('GH_USERNAME')

    if not TOKEN or not USERNAME:
        print("에러: .env 파일에 GH_TOKEN 또는 GH_USERNAME이 설정되지 않았습니다.")
    else:
        analyzer = GitHubAnalyzer(TOKEN)
        print(f"{USERNAME}님의 전체 활동 데이터를 불러오는 중...")

        exts, dates = analyzer.get_last_week_data(USERNAME)
        streak = analyzer.calculate_streak(dates)

        print(f"\n--- 분석 결과 ---")
        print(f"최근 7일간 수정된 파일 확장자 수: {len(exts)}개")
        print(f"현재 연속 커밋 기록: {streak}일 🔥")
