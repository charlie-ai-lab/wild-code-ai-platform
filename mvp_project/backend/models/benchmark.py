"""
Benchmark Data Model - Agent性能基准测试
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Dict, Any
from datetime import datetime
from enum import Enum


class BenchmarkCategory(str, Enum):
    """基准测试类别"""
    CODE_GENERATION = "code_generation"
    QA = "qa"
    REASONING = "reasoning"
    WRITING = "writing"
    TRANSLATION = "translation"
    SUMMARIZATION = "summarization"
    GENERAL = "general"


class BenchmarkStatus(str, Enum):
    """基准测试状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TestResult(BaseModel):
    """单个测试结果"""
    test_id: str
    test_name: str
    passed: bool
    score: float = Field(..., ge=0, le=1, description="得分 0-1")
    duration_seconds: float
    output: Optional[str] = None
    error: Optional[str] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)


class BenchmarkTest(BaseModel):
    """基准测试用例"""
    id: str
    name: str
    category: BenchmarkCategory
    description: str
    input_data: Dict[str, Any] = Field(default_factory=dict)
    expected_output: Optional[str] = None
    evaluation_criteria: List[str] = Field(default_factory=list)
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    max_score: float = 1.0


class AgentBenchmark(BaseModel):
    """Agent基准测试结果"""
    id: str = Field(..., description="基准测试ID")
    agent_id: str
    agent_name: str
    agent_version: Optional[str] = None
    category: BenchmarkCategory
    
    # 测试结果
    total_tests: int
    passed_tests: int
    failed_tests: int
    pass_rate: float = Field(..., ge=0, le=1, description="通过率 0-1")
    average_score: float = Field(..., ge=0, le=1, description="平均得分 0-1")
    
    # 性能指标
    total_duration_seconds: float
    average_response_time: float
    min_response_time: float
    max_response_time: float
    
    # 详细结果
    test_results: List[TestResult] = Field(default_factory=list)
    
    # 退化检测
    is_degraded: bool = False
    degradation_p_value: Optional[float] = None
    baseline_pass_rate: Optional[float] = None
    
    # 成本估算
    estimated_cost_usd: Optional[float] = None
    total_tokens: Optional[int] = None
    
    # 元数据
    status: BenchmarkStatus = BenchmarkStatus.COMPLETED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    # 额外信息
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class BenchmarkConfig(BaseModel):
    """基准测试配置"""
    agent_id: str
    agent_version: Optional[str] = None
    categories: List[BenchmarkCategory] = Field(default_factory=list)
    test_ids: Optional[List[str]] = None  # 如果指定，只运行这些测试
    max_duration_seconds: float = 300
    enable_cost_tracking: bool = True
    enable_degradation_check: bool = True
    custom_tests: Optional[List[BenchmarkTest]] = None


class BenchmarkComparison(BaseModel):
    """Agent性能对比"""
    agent_1: AgentBenchmark
    agent_2: AgentBenchmark
    comparison_score: float  # agent_1相对于agent_2的优势得分
    winner: Optional[str] = None  # 胜者的agent_id
    insights: List[str] = Field(default_factory=list)


class BenchmarkReport(BaseModel):
    """基准测试报告"""
    report_id: str
    title: str
    generated_at: datetime
    benchmarks: List[AgentBenchmark]
    rankings: List[Dict[str, Any]]  # 排名
    summary: str
    insights: List[str]
    recommendations: List[str]


class DegradationAlert(BaseModel):
    """性能退化告警"""
    alert_id: str
    agent_id: str
    agent_name: str
    category: BenchmarkCategory
    detected_at: datetime
    baseline_pass_rate: float
    current_pass_rate: float
    degradation_percentage: float
    p_value: float
    severity: Literal["low", "medium", "high", "critical"]
    recommended_actions: List[str]
