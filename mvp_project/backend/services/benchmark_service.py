"""
Benchmark Service - Agent性能基准测试服务
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from models.benchmark import (
    AgentBenchmark, BenchmarkTest, BenchmarkConfig, 
    BenchmarkCategory, BenchmarkStatus, TestResult,
    BenchmarkComparison, BenchmarkReport, DegradationAlert
)
import uuid
import time
import random
import statistics


class BenchmarkService:
    """基准测试服务类"""

    def __init__(self):
        # 内存存储
        self.benchmarks: dict[str, AgentBenchmark] = {}
        self.tests: dict[str, BenchmarkTest] = {}
        self.baselines: dict[str, float] = {}  # agent_id -> baseline pass rate
        self.alerts: list[DegradationAlert] = []
        
        # 初始化标准测试用例
        self._init_standard_tests()

    def _init_standard_tests(self):
        """初始化标准测试用例"""
        # 代码生成测试
        code_tests = [
            BenchmarkTest(
                id="code_001",
                name="Python Hello World",
                category=BenchmarkCategory.CODE_GENERATION,
                description="生成Python Hello World代码",
                input_data={"language": "python", "task": "hello world"},
                evaluation_criteria=["语法正确", "输出正确"],
                difficulty="easy",
                max_score=1.0
            ),
            BenchmarkTest(
                id="code_002",
                name="快速排序实现",
                category=BenchmarkCategory.CODE_GENERATION,
                description="实现快速排序算法",
                input_data={"language": "python", "algorithm": "quick sort"},
                evaluation_criteria=["算法正确", "时间复杂度O(n log n)", "代码可读性"],
                difficulty="medium",
                max_score=1.0
            ),
            BenchmarkTest(
                id="code_003",
                name="二叉树遍历",
                category=BenchmarkCategory.CODE_GENERATION,
                description="实现二叉树的中序遍历",
                input_data={"data_structure": "binary tree", "traversal": "inorder"},
                evaluation_criteria=["算法正确", "递归实现", "处理边界情况"],
                difficulty="medium",
                max_score=1.0
            ),
        ]

        # QA测试
        qa_tests = [
            BenchmarkTest(
                id="qa_001",
                name="基础问答",
                category=BenchmarkCategory.QA,
                description="回答简单的常识问题",
                input_data={"question": "巴黎是哪个国家的首都？"},
                expected_output="法国",
                evaluation_criteria=["答案准确", "表述清晰"],
                difficulty="easy",
                max_score=1.0
            ),
            BenchmarkTest(
                id="qa_002",
                name="数学计算",
                category=BenchmarkCategory.QA,
                description="解决数学问题",
                input_data={"question": "计算 123 × 456"},
                expected_output="56088",
                evaluation_criteria=["计算正确", "步骤清晰"],
                difficulty="medium",
                max_score=1.0
            ),
        ]

        # 推理测试
        reasoning_tests = [
            BenchmarkTest(
                id="reason_001",
                name="逻辑推理",
                category=BenchmarkCategory.REASONING,
                description="逻辑推理题",
                input_data={"problem": "如果A>B，B>C，那么A和C的关系？"},
                evaluation_criteria=["推理正确", "逻辑严密"],
                difficulty="easy",
                max_score=1.0
            ),
        ]

        # 注册所有测试
        all_tests = code_tests + qa_tests + reasoning_tests
        for test in all_tests:
            self.tests[test.id] = test

    async def list_tests(self, category: Optional[BenchmarkCategory] = None) -> List[BenchmarkTest]:
        """列出所有测试用例"""
        tests = list(self.tests.values())
        if category:
            tests = [t for t in tests if t.category == category]
        return tests

    async def get_test(self, test_id: str) -> Optional[BenchmarkTest]:
        """获取测试用例"""
        return self.tests.get(test_id)

    async def list_benchmarks(self, agent_id: Optional[str] = None, 
                               category: Optional[BenchmarkCategory] = None) -> List[AgentBenchmark]:
        """列出所有基准测试"""
        benchmarks = list(self.benchmarks.values())
        
        if agent_id:
            benchmarks = [b for b in benchmarks if b.agent_id == agent_id]
        if category:
            benchmarks = [b for b in benchmarks if b.category == category]
        
        # 按创建时间倒序
        benchmarks.sort(key=lambda b: b.created_at, reverse=True)
        return benchmarks

    async def get_benchmark(self, benchmark_id: str) -> Optional[AgentBenchmark]:
        """获取基准测试结果"""
        return self.benchmarks.get(benchmark_id)

    async def run_benchmark(self, config: BenchmarkConfig, agent_name: str) -> AgentBenchmark:
        """运行基准测试"""
        benchmark_id = str(uuid.uuid4())
        
        # 选择测试用例
        if config.test_ids:
            tests_to_run = [self.tests[tid] for tid in config.test_ids if tid in self.tests]
        else:
            tests_to_run = list(self.tests.values())
            if config.categories:
                tests_to_run = [t for t in tests_to_run if t.category in config.categories]

        if not tests_to_run:
            raise ValueError("No tests to run")

        # 初始化基准测试
        benchmark = AgentBenchmark(
            id=benchmark_id,
            agent_id=config.agent_id,
            agent_name=agent_name,
            agent_version=config.agent_version,
            category=tests_to_run[0].category,
            total_tests=len(tests_to_run),
            passed_tests=0,
            failed_tests=0,
            pass_rate=0.0,
            average_score=0.0,
            total_duration_seconds=0.0,
            average_response_time=0.0,
            min_response_time=float('inf'),
            max_response_time=0.0,
            status=BenchmarkStatus.RUNNING,
            created_at=datetime.utcnow()
        )
        
        self.benchmarks[benchmark_id] = benchmark

        # 运行测试
        test_results = []
        response_times = []
        
        for test in tests_to_run:
            result = await self._run_single_test(test, config.agent_id)
            test_results.append(result)
            response_times.append(result.duration_seconds)
            
            # 更新统计
            if result.passed:
                benchmark.passed_tests += 1
            else:
                benchmark.failed_tests += 1
            
            # 更新响应时间
            benchmark.total_duration_seconds += result.duration_seconds

        # 计算统计指标
        if response_times:
            benchmark.average_response_time = statistics.mean(response_times)
            benchmark.min_response_time = min(response_times)
            benchmark.max_response_time = max(response_times)
        
        benchmark.test_results = test_results
        benchmark.pass_rate = benchmark.passed_tests / benchmark.total_tests
        benchmark.average_score = sum(r.score for r in test_results) / len(test_results)
        
        # 退化检测
        if config.enable_degradation_check and config.agent_id in self.baselines:
            baseline_rate = self.baselines[config.agent_id]
            benchmark.baseline_pass_rate = baseline_rate
            benchmark.is_degraded = benchmark.pass_rate < baseline_rate * 0.95  # 下降5%视为退化
            # TODO: 实现统计显著性测试

        # 成本估算
        if config.enable_cost_tracking:
            benchmark.estimated_cost_usd = benchmark.total_tests * 0.001  # 模拟成本
            benchmark.total_tokens = benchmark.total_tests * 100  # 模拟token数

        benchmark.status = BenchmarkStatus.COMPLETED
        benchmark.completed_at = datetime.utcnow()
        
        # 更新基准线（如果是第一次运行，或性能更好）
        if config.agent_id not in self.baselines or benchmark.pass_rate > self.baselines[config.agent_id]:
            self.baselines[config.agent_id] = benchmark.pass_rate

        return benchmark

    async def _run_single_test(self, test: BenchmarkTest, agent_id: str) -> TestResult:
        """
        运行单个测试
        
        TODO: 实现真实的Agent调用逻辑
        当前使用模拟数据
        """
        start_time = time.time()
        
        # 模拟Agent响应
        # 模拟成功率 80%
        passed = random.random() < 0.8
        score = random.uniform(0.7, 1.0) if passed else random.uniform(0.0, 0.5)
        duration = random.uniform(0.5, 3.0)
        
        end_time = time.time()
        
        result = TestResult(
            test_id=test.id,
            test_name=test.name,
            passed=passed,
            score=score,
            duration_seconds=end_time - start_time,
            output="模拟输出" if passed else None,
            error="模拟错误" if not passed else None,
            metrics={
                "difficulty": test.difficulty,
                "agent_id": agent_id,
                "category": test.category
            }
        )
        
        return result

    async def compare_agents(self, agent_1_id: str, agent_2_id: str, 
                            category: BenchmarkCategory) -> Optional[BenchmarkComparison]:
        """对比两个Agent的性能"""
        # 获取两个Agent的最新测试结果
        agent_1_benchmarks = [b for b in await self.list_benchmarks(agent_1_id, category)]
        agent_2_benchmarks = [b for b in await self.list_benchmarks(agent_2_id, category)]
        
        if not agent_1_benchmarks or not agent_2_benchmarks:
            return None
        
        agent_1_latest = agent_1_benchmarks[0]  # 最新的
        agent_2_latest = agent_2_benchmarks[0]
        
        # 计算对比得分
        comparison_score = agent_1_latest.average_score - agent_2_latest.average_score
        winner = agent_1_id if comparison_score > 0 else agent_2_id if comparison_score < 0 else None
        
        # 生成洞察
        insights = []
        insights.append(f"{agent_1_latest.agent_name} 平均得分: {agent_1_latest.average_score:.2%}")
        insights.append(f"{agent_2_latest.agent_name} 平均得分: {agent_2_latest.average_score:.2%}")
        insights.append(f"响应时间差异: {abs(agent_1_latest.average_response_time - agent_2_latest.average_response_time):.2f}秒")
        
        if agent_1_latest.pass_rate != agent_2_latest.pass_rate:
            insights.append(f"通过率差异: {abs(agent_1_latest.pass_rate - agent_2_latest.pass_rate):.1%}")
        
        comparison = BenchmarkComparison(
            agent_1=agent_1_latest,
            agent_2=agent_2_latest,
            comparison_score=comparison_score,
            winner=winner,
            insights=insights
        )
        
        return comparison

    async def generate_report(self, category: Optional[BenchmarkCategory] = None) -> Optional[BenchmarkReport]:
        """生成基准测试报告"""
        benchmarks = await self.list_benchmarks(category=category)

        if not benchmarks:
            return None

        # 按Agent分组
        agent_scores = {}
        for b in benchmarks:
            if b.agent_id not in agent_scores:
                agent_scores[b.agent_id] = {
                    "agent_id": b.agent_id,
                    "agent_name": b.agent_name,
                    "avg_score": 0.0,
                    "pass_rate": 0.0,
                    "count": 0
                }
            agent_data = agent_scores[b.agent_id]
            agent_data["avg_score"] += b.average_score
            agent_data["pass_rate"] += b.pass_rate
            agent_data["count"] += 1

        # 计算平均分
        for agent_data in agent_scores.values():
            agent_data["avg_score"] /= agent_data["count"]
            agent_data["pass_rate"] /= agent_data["count"]

        # 排名
        rankings = sorted(agent_scores.values(), key=lambda x: x["avg_score"], reverse=True)

        # 生成总结
        top_agent = rankings[0]
        summary = f"本次测试共{len(benchmarks)}个基准测试，涵盖{len(agent_scores)}个Agent。"
        summary += f" 最佳Agent是 {top_agent['agent_name']}，平均得分 {top_agent['avg_score']:.1%}。"

        # 生成洞察
        insights = []
        insights.append(f"平均响应时间: {statistics.mean([b.average_response_time for b in benchmarks]):.2f}秒")
        insights.append(f"平均通过率: {statistics.mean([b.pass_rate for b in benchmarks]):.1%}")

        # 性能退化检查
        degraded_count = sum(1 for b in benchmarks if b.is_degraded)
        if degraded_count > 0:
            insights.append(f"⚠️ 检测到 {degraded_count} 个Agent性能退化")

        # 生成建议
        recommendations = []
        if top_agent["avg_score"] < 0.8:
            recommendations.append("所有Agent性能有待提升，建议优化提示词和上下文管理")
        if benchmarks and benchmarks[0].average_response_time > 2.0:
            recommendations.append("响应时间较长，建议考虑缓存和批处理优化")

        report = BenchmarkReport(
            report_id=str(uuid.uuid4()),
            title=f"Agent性能基准测试报告 - {datetime.utcnow().strftime('%Y-%m-%d')}",
            generated_at=datetime.utcnow(),
            benchmarks=benchmarks,
            rankings=rankings,
            summary=summary,
            insights=insights,
            recommendations=recommendations
        )

        return report

    async def check_degradation_alerts(self) -> List[DegradationAlert]:
        """检查性能退化告警"""
        alerts = []
        
        for benchmark in await self.list_benchmarks():
            if benchmark.is_degraded and benchmark.baseline_pass_rate:
                degradation_pct = (benchmark.baseline_pass_rate - benchmark.pass_rate) / benchmark.baseline_pass_rate * 100
                
                # 确定严重程度
                if degradation_pct > 20:
                    severity = "critical"
                elif degradation_pct > 10:
                    severity = "high"
                elif degradation_pct > 5:
                    severity = "medium"
                else:
                    severity = "low"
                
                alert = DegradationAlert(
                    alert_id=str(uuid.uuid4()),
                    agent_id=benchmark.agent_id,
                    agent_name=benchmark.agent_name,
                    category=benchmark.category,
                    detected_at=benchmark.completed_at or datetime.utcnow(),
                    baseline_pass_rate=benchmark.baseline_pass_rate,
                    current_pass_rate=benchmark.pass_rate,
                    degradation_percentage=degradation_pct,
                    p_value=benchmark.degradation_p_value or 0.0,
                    severity=severity,
                    recommended_actions=[
                        "检查Agent配置和提示词",
                        "验证API密钥和权限",
                        "联系服务商确认系统状态",
                        "考虑切换到备用Agent"
                    ]
                )
                
                alerts.append(alert)
        
        self.alerts = alerts
        return alerts


# 全局基准测试服务实例
benchmark_service = BenchmarkService()
