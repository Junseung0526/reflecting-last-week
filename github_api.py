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
        event_count = 0
        push_event_count = 0
        recent_push_count = 0
        commit_payload_count = 0
        file_count = 0

        for event in events:
            event_count += 1
            if event.type == "PushEvent":
                push_event_count += 1
                commit_dates.add(event.created_at.date())

                if event.created_at >= seven_days_ago:
                    recent_push_count += 1

                    # repo 객체를 제대로 가져오기
                    try:
                        repo = self.g.get_repo(event.repo.name)
                    except Exception as e:
                        print(f"⚠️ Repo 접근 실패 ({event.repo.name}): {e}")
                        continue

                    # head SHA로 커밋 가져오기
                    try:
                        head_sha = event.payload.get('head')
                        if not head_sha:
                            continue

                        commit = repo.get_commit(head_sha)
                        commit_payload_count += 1

                        for file in commit.files:
                            filename = file.filename
                            if '.' in filename:
                                ext = "." + filename.split('.')[-1].lower()
                                extensions.append(ext)
                                file_count += 1
                            else:
                                extensions.append(filename)
                                file_count += 1
                    except Exception as e:
                        print(f"⚠️ 커밋 처리 중 에러 (SHA: {head_sha[:7] if head_sha else 'N/A'}): {e}")
                        continue

        print(f"📊 수집 완료: 이벤트 {event_count}개 | PushEvent {push_event_count}개 | 최근 7일 Push {recent_push_count}개 | 커밋 {commit_payload_count}개 | 파일 {file_count}개")


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
