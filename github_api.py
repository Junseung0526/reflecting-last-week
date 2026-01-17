import datetime
import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

class GitHubAnalyzer:
    def __init__(self, token):
        self.g = Github(token)

    def get_last_week_data(self, username):
        """
        최근 7일간의 커밋 파일 확장자 통계와 커밋 날짜를 가져옵니다.
        """
        user = self.g.get_user(username)
        seven_days_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)

        extensions = []
        commit_dates = set()

        # 사용자의 최근 이벤트 가져오기
        events = user.get_events()

        for event in events:
            # 이벤트 생성 시간이 7일 이전이면 루프 종료
            if event.created_at < seven_days_ago:
                break

            if event.type == "PushEvent":
                # 커밋 날짜 저장
                commit_dates.add(event.created_at.date())

                repo = event.repo
                for commit_payload in event.payload.get('commits', []):
                    try:
                        # 각 커밋에서 수정된 파일 목록 가져오기
                        commit = repo.get_commit(commit_payload['sha'])
                        for file in commit.files:
                            filename = file.filename
                            if '.' in filename:
                                ext = "." + filename.split('.')[-1].lower()
                                extensions.append(ext)
                            else:
                                # 확장자가 없는 파일
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
        print(f"{USERNAME}님의 데이터를 분석 중입니다...")

        exts, dates = analyzer.get_last_week_data(USERNAME)
        streak = analyzer.calculate_streak(dates)

        print(f"--- 분석 결과 ---")
        print(f"최근 7일간 수정된 파일 확장자 수: {len(exts)}개")
        print(f"현재 연속 커밋 기록: {streak}일")