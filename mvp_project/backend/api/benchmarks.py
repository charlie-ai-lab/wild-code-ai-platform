"""
Benchmark API Routes - Agent性能基准测试API
"""
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from typing import List, Optional
from models.benchmark import (
    BenchmarkTest, AgentBenchmark, BenchmarkConfig, 
    BenchmarkCategory, BenchmarkComparison, BenchmarkReport,
    DegradationAlert
)
from services.benchmark_service import benchmark_service

router = APIRouter(prefix="/benchmarks", tags=["Benchmarks"])


# ==================== 测试用例管理 ====================

@router.get("/tests", response_model=List[BenchmarkTest], summary="列出所有测试用例")
async def list_tests(category: Optional[BenchmarkCategory] = None):
    """
    列出所有可用的测试用例

    - **category**: 可选，按类别筛选
    """
    return await benchmark_service.list_tests(category)


@router.get("/tests/{test_id}", response_model=BenchmarkTest, summary="获取测试用例详情")
async def get_test(test_id: str):
    """获取指定测试用例的详细信息"""
    test = await benchmark_service.get_test(test_id)
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Test {test_id} not found"
        )
    return test


# ==================== 基准测试执行 ====================

@router.get("/rankings", summary="获取Agent性能排名")
async def get_rankings(
    category: Optional[BenchmarkCategory] = None,
    limit: int = 10
):
    """
    获取Agent性能排名

    - **category**: 可选，按类别筛选
    - **limit**: 返回前N名
    """
    report = await benchmark_service.generate_report(category)

    if not report or not report.rankings:
        # 返回空排名
        return {
            "category": category or "all",
            "generated_at": None,
            "total_agents": 0,
            "rankings": []
        }

    rankings = report.rankings[:limit]

    return {
        "category": category or "all",
        "generated_at": report.generated_at.isoformat(),
        "total_agents": len(rankings),
        "rankings": [
            {
                "rank": i + 1,
                "agent_id": r["agent_id"],
                "agent_name": r["agent_name"],
                "avg_score": f"{r['avg_score']:.1%}",
                "pass_rate": f"{r['pass_rate']:.1%}"
            }
            for i, r in enumerate(rankings[:limit])
        ]
    }


@router.get("", response_model=List[AgentBenchmark], summary="列出所有基准测试")
async def list_benchmarks(
    agent_id: Optional[str] = None,
    category: Optional[BenchmarkCategory] = None
):
    """
    列出所有基准测试结果

    - **agent_id**: 可选，按Agent筛选
    - **category**: 可选，按类别筛选
    """
    return await benchmark_service.list_benchmarks(agent_id, category)


@router.get("/{benchmark_id}", response_model=AgentBenchmark, summary="获取基准测试结果")
async def get_benchmark(benchmark_id: str):
    """获取指定基准测试的详细信息"""
    benchmark = await benchmark_service.get_benchmark(benchmark_id)
    if not benchmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Benchmark {benchmark_id} not found"
        )
    return benchmark


@router.post("/run", response_model=AgentBenchmark, summary="运行基准测试")
async def run_benchmark(config: BenchmarkConfig, background_tasks: BackgroundTasks):
    """
    运行Agent基准测试

    - **agent_id**: Agent唯一标识
    - **agent_version**: 可选，Agent版本
    - **categories**: 可选，测试类别列表
    - **test_ids**: 可选，指定测试用例ID
    - **max_duration_seconds**: 最大运行时间
    - **enable_cost_tracking**: 启用成本跟踪
    - **enable_degradation_check**: 启用退化检测
    """
    # 这里简化处理，实际应该通过agent_id获取agent_name
    # 可以调用agent_service获取
    agent_name = f"Agent-{config.agent_id}"
    
    try:
        benchmark = await benchmark_service.run_benchmark(config, agent_name)
        return benchmark
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ==================== 性能对比 ====================

@router.post("/compare", response_model=BenchmarkComparison, summary="对比Agent性能")
async def compare_agents(
    agent_1_id: str,
    agent_2_id: str,
    category: BenchmarkCategory
):
    """
    对比两个Agent的性能

    - **agent_1_id**: 第一个Agent ID
    - **agent_2_id**: 第二个Agent ID
    - **category**: 测试类别
    """
    comparison = await benchmark_service.compare_agents(agent_1_id, agent_2_id, category)
    if not comparison:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Benchmark data not found for one or both agents"
        )
    return comparison


# ==================== 报告生成 ====================

@router.get("/reports/latest", summary="获取最新基准测试报告")
async def get_latest_report(category: Optional[BenchmarkCategory] = None):
    """
    生成并获取最新的基准测试报告

    - **category**: 可选，按类别筛选
    """
    benchmarks = await benchmark_service.list_benchmarks(category=category)
    
    if not benchmarks:
        return {
            "message": "No benchmark data available yet. Run some benchmarks first.",
            "total_benchmarks": 0,
            "total_agents": 0
        }
    
    try:
        report = await benchmark_service.generate_report(category)
        return report
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ==================== 退化检测和告警 ====================

@router.get("/alerts/degradation", response_model=List[DegradationAlert], summary="获取性能退化告警")
async def get_degradation_alerts():
    """
    获取所有性能退化告警
    """
    return await benchmark_service.check_degradation_alerts()


# ==================== 统计数据 ====================

@router.get("/stats/summary", summary="获取统计数据摘要")
async def get_summary_stats():
    """获取基准测试统计数据摘要"""
    benchmarks = await benchmark_service.list_benchmarks()
    
    if not benchmarks:
        return {
            "total_benchmarks": 0,
            "total_agents": 0,
            "avg_pass_rate": 0,
            "avg_score": 0,
            "total_tests": 0
        }
    
    from statistics import mean
    
    # 按Agent分组
    agents = set(b.agent_id for b in benchmarks)
    
    return {
        "total_benchmarks": len(benchmarks),
        "total_agents": len(agents),
        "avg_pass_rate": mean(b.pass_rate for b in benchmarks),
        "avg_score": mean(b.average_score for b in benchmarks),
        "avg_response_time": mean(b.average_response_time for b in benchmarks),
        "total_tests": sum(b.total_tests for b in benchmarks),
        "total_passed": sum(b.passed_tests for b in benchmarks),
        "degraded_count": sum(1 for b in benchmarks if b.is_degraded)
    }
