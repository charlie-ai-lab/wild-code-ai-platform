/** @type {import('.ts')} */
import { Inter } from 'next/font/google';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <meta charSet="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>野码AI - AI Agent Collaboration Platform</title>
        <style>{`
          * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
          }
          body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
              'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
              sans-serif;
            background: #0a0a0a;
            color: #333;
            line-height: 1.6;
          }
          .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
          }
          .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
          }
          .header h1 {
            margin: 0;
            font-size: 1.75rem;
            font-weight: 700;
          }
          .content {
            background: white;
            border-radius: 0.5rem;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
          }
          .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
          }
          .card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 0.5rem;
            padding: 1.5rem;
            transition: all 0.2s;
            cursor: pointer;
          }
          .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
          }
          .card h3 {
            margin: 0 0 0.75rem;
            font-size: 1.25rem;
            font-weight: 600;
            color: #1a1a1a;
          }
          .card p {
            color: #666;
            line-height: 1.6;
            margin-bottom: 1rem;
          }
          .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: #667eea;
            color: white;
            border-radius: 1rem;
            font-size: 0.75rem;
            font-weight: 600;
          }
        `}</style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>🤖 野码AI - AI Agent Collaboration Platform</h1>
            <p>多AI Agent统一协作平台</p>
          </div>
          
          <div class="content">
            <div class="grid">
              <div class="card">
                <h3>🎯 核心功能</h3>
                <p>支持Claude Code、Gemini CLI、OpenCode、CodeBuddy等多个AI Agent</p>
                <p><span class="badge">31</span> 已集成Agents</p>
              </div>
              
              <div class="card">
                <h3>📝 技能栈</h3>
                <p>Python 3.12 + FastAPI 0.104</p>
                <p>Next.js 15 + TypeScript 5</p>
                <p>PostgreSQL 16 + Redis 7.4</p>
              </div>
              
              <div class="card">
                <h3>🔧 开发工具</h3>
                <p>GitHub Actions、CI/CD</p>
                <p><span class="badge">17</span> 个Skills</p>
              </div>
              
              <div class="card">
                <h3>🔍 搜索工具</h3>
                <p>Tavily、Twitter、Reddit</p>
                <p><span class="badge">6</span> 个Skills</p>
              </div>
            </div>
          </div>
        </div>
        
        <script src="https://cdn.tailwindcss.com"></script>
      </body>
    </html>
  );
}
