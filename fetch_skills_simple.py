#!/usr/bin/env python3
import json
import subprocess
import sys

# 尝试使用curl从skills.sh API获取数据
def get_skills_from_api():
    try:
        # 使用curl获取skills.sh trending数据
        cmd = [
            'curl', '-s',
            'https://api.skills.sh/trending',
            '-H', 'Accept: application/json'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            # 获取trulyTrendingSkills中的前15个
            if 'trulyTrendingSkills' in data:
                skills = data['trulyTrendingSkills'][:15]
                print("✅ 成功获取top 15热门skills:\n")
                for i, skill in enumerate(skills, 1):
                    print(f"{i}. {skill['source']}/{skill['skillId']}")
                    print(f"   名称: {skill['name']}")
                    print(f"   安装次数: {skill['installs']}")
                    print()
                return skills
            else:
                print("❌ API数据格式异常")
                return None
        else:
            print(f"❌ curl失败: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

if __name__ == '__main__':
    skills = get_skills_from_api()
    if skills:
        print(f"\n📊 共找到 {len(skills)} 个热门skills")
