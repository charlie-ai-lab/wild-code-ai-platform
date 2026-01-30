'use client'

import { useEffect, useState } from 'react'

interface AgentRanking {
  rank: number
  agent_id: string
  agent_name: string
  avg_score: string
  pass_rate: string
}

interface RankingResponse {
  category: string
  generated_at: string | null
  total_agents: number
  rankings: AgentRanking[]
}

export default function Dashboard() {
  const [rankings, setRankings] = useState<AgentRanking[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchRankings()
    const interval = setInterval(fetchRankings, 60000) // 每分钟刷新
    return () => clearInterval(interval)
  }, [])

  const fetchRankings = async () => {
    try {
      const response = await fetch('http://localhost:8000/benchmarks/rankings?limit=10')
      if (!response.ok) throw new Error('获取排名失败')
      const data: RankingResponse = await response.json()
      setRankings(data.rankings)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : '未知错误')
    } finally {
      setLoading(false)
    }
  }

  const runBenchmark = async (agentId: string) => {
    try {
      const response = await fetch('http://localhost:8000/benchmarks/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent_id: agentId }),
      })
      if (!response.ok) throw new Error('运行测试失败')
      const result = await response.json()
      alert(`测试完成！\n平均得分: ${(result.average_score * 100).toFixed(1)}%\n通过率: ${(result.pass_rate * 100).toFixed(1)}%`)
      fetchRankings() // 刷新排名
    } catch (err) {
      alert('运行测试失败: ' + (err instanceof Error ? err.message : '未知错误'))
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            ⚡ 野码AI - Agent性能基准测试
          </h1>
          <p className="text-xl text-purple-200">
            统一的多AI Agent协作平台 + Agent性能基准测试
          </p>
        </header>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-purple-500"></div>
            <p className="mt-4 text-purple-200">加载中...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-500/20 border border-red-500 text-red-200 px-4 py-3 rounded mb-6">
            ⚠️ {error}
            <button
              onClick={fetchRankings}
              className="ml-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
            >
              重试
            </button>
          </div>
        )}

        {/* Rankings Table */}
        {!loading && !error && (
          <>
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 shadow-2xl border border-purple-500/20">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold text-white">🏆 Agent性能排名</h2>
                <button
                  onClick={fetchRankings}
                  className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
                >
                  🔄 刷新
                </button>
              </div>

              {rankings.length === 0 ? (
                <div className="text-center py-12 text-purple-200">
                  <p className="text-xl mb-4">暂无排名数据</p>
                  <button
                    onClick={() => runBenchmark('claude_code')}
                    className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700"
                  >
                    🚀 运行测试
                  </button>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-purple-500/30">
                        <th className="text-left py-4 px-6 text-purple-200 font-semibold">排名</th>
                        <th className="text-left py-4 px-6 text-purple-200 font-semibold">Agent名称</th>
                        <th className="text-left py-4 px-6 text-purple-200 font-semibold">平均得分</th>
                        <th className="text-left py-4 px-6 text-purple-200 font-semibold">通过率</th>
                        <th className="text-left py-4 px-6 text-purple-200 font-semibold">操作</th>
                      </tr>
                    </thead>
                    <tbody>
                      {rankings.map((agent, index) => (
                        <tr
                          key={agent.agent_id}
                          className={`border-b border-purple-500/20 hover:bg-purple-500/10 transition-colors ${
                            index === 0 ? 'bg-yellow-500/10' : ''
                          }`}
                        >
                          <td className="py-4 px-6">
                            {index === 0 && <span className="text-2xl">🥇</span>}
                            {index === 1 && <span className="text-2xl">🥈</span>}
                            {index === 2 && <span className="text-2xl">🥉</span>}
                            {index > 2 && (
                              <span className="text-xl font-bold text-purple-300">#{agent.rank}</span>
                            )}
                          </td>
                          <td className="py-4 px-6 text-white font-medium">{agent.agent_name}</td>
                          <td className="py-4 px-6">
                            <div className="flex items-center gap-2">
                              <div className="w-24 bg-slate-700 rounded-full h-2">
                                <div
                                  className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full"
                                  style={{ width: agent.avg_score }}
                                ></div>
                              </div>
                              <span className="text-purple-200 font-mono">{agent.avg_score}</span>
                            </div>
                          </td>
                          <td className="py-4 px-6">
                            <span className="text-purple-200 font-mono">{agent.pass_rate}</span>
                          </td>
                          <td className="py-4 px-6">
                            <button
                              onClick={() => runBenchmark(agent.agent_id)}
                              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
                            >
                              🧪 测试
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-purple-500/20">
                <h3 className="text-xl font-bold text-white mb-4">📊 运行新测试</h3>
                <p className="text-purple-200 mb-4">为Agent运行性能基准测试</p>
                <div className="flex gap-2">
                  {['claude_code', 'gemini_cli', 'open_code', 'codebuddy'].map((agent) => (
                    <button
                      key={agent}
                      onClick={() => runBenchmark(agent)}
                      className="px-3 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 text-sm transition-colors"
                    >
                      {agent}
                    </button>
                  ))}
                </div>
              </div>

              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-purple-500/20">
                <h3 className="text-xl font-bold text-white mb-4">📈 查看报告</h3>
                <p className="text-purple-200 mb-4">查看最新的性能测试报告</p>
                <button className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
                  查看报告
                </button>
              </div>

              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-purple-500/20">
                <h3 className="text-xl font-bold text-white mb-4">⚠️ 告警信息</h3>
                <p className="text-purple-200 mb-4">查看性能退化告警</p>
                <button className="w-full px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors">
                  查看告警
                </button>
              </div>
            </div>

            {/* Footer */}
            <footer className="mt-12 text-center text-purple-200">
              <p>
                🚀 野码AI - Agent性能基准测试平台 |{' '}
                <a
                  href="https://github.com/charlie-ai-lab/wild-code-ai-platform"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-purple-400 hover:text-purple-300 underline"
                >
                  GitHub
                </a>
              </p>
            </footer>
          </>
        )}
      </div>
    </div>
  )
}
