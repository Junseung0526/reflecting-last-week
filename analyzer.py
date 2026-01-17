import json
import os


class StatsAnalyzer:
    def __init__(self, mapping_path='mappings.json'):

        current_dir = os.getcwd()
        actual_path = os.path.join(current_dir, mapping_path)

        if not os.path.exists(actual_path):
            base_path = os.path.dirname(os.path.abspath(__file__))
            actual_path = os.path.join(base_path, mapping_path)

        if not os.path.exists(actual_path):
            raise FileNotFoundError(f"'{mapping_path}' 파일을 찾을 수 없습니다. 위치를 확인해주세요: {actual_path}")

        with open(actual_path, 'r', encoding='utf-8') as f:
            self.mapping = json.load(f)

    def analyze_categories(self, extensions):
        """
        확장자 리스트를 바탕으로 카테고리별 비중을 계산합니다.
        """
        if not extensions:
            return {}

        category_counts = {key: 0 for key in self.mapping.keys()}
        total_matched = 0

        for ext in extensions:
            matched = False
            for category, ext_list in self.mapping.items():
                if ext in ext_list:
                    category_counts[category] += 1
                    total_matched += 1
                    matched = True
                    break


        if total_matched == 0:
            return {}

        stats = {}
        for category, count in category_counts.items():
            percentage = (count / total_matched) * 100
            if percentage > 0:
                stats[category] = round(percentage, 1)

        return dict(sorted(stats.items(), key=lambda item: item[1], reverse=True))

    def format_gist_text(self, stats, streak, top_language):
        """
        Gist에 박제할 최종 텍스트 레이아웃을 만듭니다.
        """
        lines = []
        lines.append("📅 ReflectingLastWeek (Last 7 Days)")
        lines.append("")

        lines.append(f"🏆 TOP LANGUAGE: {top_language}")
        lines.append("")

        lines.append("🛠 FOCUS AREA")
        for category, percent in stats.items():
            bar_length = int(percent / 10)
            bar = "█" * bar_length + "░" * (10 - bar_length)
            lines.append(f"{category:<12} {bar} {percent}%")

        lines.append("")
        lines.append("🔥 STREAK STATUS")
        lines.append(f"1일 1커밋 연속 {streak}일째 순항 중!")

        return "\n".join(lines)