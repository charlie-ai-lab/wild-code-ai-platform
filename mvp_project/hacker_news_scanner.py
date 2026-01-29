"""
Hacker News Scanner - 野码AI
获取和分析Hacker News热门故事，发现技术趋势和市场机会
"""
import json
import subprocess
from datetime import datetime

def get_hacker_news_top_stories():
    """获取Hacker News Top Stories"""
    try:
        result = subprocess.run(
            ['curl', '-s', 'https://hacker-news.firebaseio.com/v0/topstories.json'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            stories = json.loads(result.stdout)
            return stories[:10]  # 返回前10个
        return []
    
    except Exception as e:
        print(f"❌ 获取Hacker News失败: {e}")
        return []

def get_story_details(story_id):
    """获取单个story的详细信息"""
    try:
        result = subprocess.run(
            ['curl', '-s', f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        return None
    
    except Exception as e:
        print(f"❌ 获取story详情失败: {e}")
        return None

def scan_hacker_news():
    """扫描Hacker News热门故事"""
    print("🔥 Hacker News Scanner")
    print("="*80)
    
    # 获取Top Stories
    stories = get_hacker_news_top_stories()
    
    if not stories:
        print("❌ 无法获取Hacker News数据")
        return
    
    # 获取前5个stories的详细信息
    print(f"\n📊 Top 5 Stories Analysis:")
    print("="*80)
    
    for i, story_id in enumerate(stories[:5], 1):
        story = get_story_details(story_id)
        
        if story:
            title = story.get('title', 'Unknown')[:70]
            url = story.get('url', 'Unknown')
            score = story.get('score', 0)
            
            print(f"\n{i}. {title}")
            print(f"   🔗 URL: {url}")
            print(f"   ⭐ Score: {score}")
            
            # 分析技术相关性
            tech_keywords = ['Claude', 'OpenAI', 'AI', 'LLM', 'API', 'benchmark', 'performance', 'testing', 'code', 'open-source']
            
            relevance = 0
            for keyword in tech_keywords:
                if keyword.lower() in title.lower():
                    relevance += 1
            
            if relevance >= 2:
                print(f"   🎯 技术相关性: 高 ({relevance}关键词匹配)")
            elif relevance == 1:
                print(f"   🔍 技术相关性: 中 ({relevance}关键词匹配)")
            else:
                print(f"   📊 技术相关性: 低")
    
    # 市场机会评估
    print("\n\n💡 市场机会评估:")
    print("="*80)
    
    # 检查是否有AI相关故事
    ai_relevant_stories = 0
    for story_id in stories[:10]:
        story = get_story_details(story_id)
        if story and any(keyword.lower() in story.get('title', '').lower() for keyword in ['Claude', 'OpenAI', 'AI', 'LLM', 'Anthropic', 'LLM benchmark']):
            ai_relevant_stories += 1
    
    if ai_relevant_stories >= 2:
        print("📈 AI技术趋势: 多个AI相关故事在热门榜单")
        print("   建议关注: AI性能测试、Agent平台、多AI集成")
    else:
        print("📉 AI技术趋势: AI相关故事较少")
        print("   建议关注: 通用开发工具、自动化、性能优化")
    
    return True

if __name__ == "__main__":
    scan_hacker_news()
    
    print("\n✅ 扫描完成")
    print(f"扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
