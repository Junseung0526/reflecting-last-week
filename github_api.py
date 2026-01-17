import datetime
import os
from github import Github


class GitHubAnalyzer:
    def __init__(self, token):
        self.g = Github(token)

    def get_last_week_data(self, username):
        """
        최근 7일간의 커밋 파일 확장자 통계와 커밋 날짜를 가져옵니다.
        """
        user = self.g.get_user(username)
        seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)

        extensions = []
        commit_dates = set()

        # 사용자의 최근 이벤트 가져오기
        events = user.get_events()

        for event in events:
            # 7일 이전 데이터면 중단
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
