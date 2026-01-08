from pydantic import BaseModel, Field
from typing import List, Optional
from typing_extensions import Literal

class Identifiers(BaseModel):
    # 测试结果的唯一标识符
    uuid: str = Field(..., description="测试结果的唯一标识符")

    # 用于 Allure Report 的标识符，表示历史测试记录
    historyId: str = Field(...,
                           description="用于 Allure Report 的标识符，表示历史测试记录")

    # 用于 Allure TestOps 的标识符，用于表示同一测试的多次执行
    testCaseId: str = Field(...,
                            description="用于 Allure TestOps 的标识符，用于表示同一测试的多次执行")


class Link(BaseModel):
    type: str
    name: str
    url: str


class Label(BaseModel):
    name: str
    value: str


class parameter(BaseModel):
    name: str
    value: str


class attachment(BaseModel):
    name: str
    source : str
    type: str

class MetaData(BaseModel):
    # 测试或步骤的标题或名称
    name: str = Field(..., description="测试的标题或步骤的名称")

    # 测试或步骤的完整名称，通常由文件名和测试名组成
    fullName: str = Field(..., description="基于文件名和测试名的唯一标识符")

    # 测试或步骤的描述，Markdown 格式
    description: Optional[str] = Field(default=None, description="测试或步骤的描述，Markdown 格式")

    # 为测试或步骤添加的链接
    links: List[Link] = Field(default_factory=list, description="为测试或步骤添加的一系列链接")

    labels: List[Label] = Field(default_factory=list, description="在测试或步骤中添加的各种标签")

    parameters: List[parameter] = Field(default_factory=list, description="测试或步骤的参数")

    attachments: List[attachment] = Field(default_factory=list, description="测试或步骤的附件")


class StatusDetails(BaseModel):
    # 标记测试失败是否由已知错误引起
    known: bool = Field(default=False, description="表示测试失败是由于已知的错误。")

    # 是否静音处理此测试结果
    muted: bool = Field(default=False, description="表示该结果不应影响统计数据。")

    # 是否是“不稳定”的测试，意味着每次执行的结果可能会不一样
    flaky: bool = Field(default=False, description="表示该测试或步骤已知不稳定，可能并非每次都成功。")

    # 失败时的简短信息，通常是异常类型
    message: Optional[str] = Field(default=None, description="测试失败时显示的简短消息，通常是导致失败的异常名称。")

    # 显示失败时的堆栈跟踪，便于调试
    trace: Optional[str] = Field(default=None, description="用于测试细节显示的全堆栈跟踪。")


class Step(BaseModel):
    # 步骤名称
    name: str
    ###
    parameters: List[parameter] = Field(default_factory=list, description="测试或步骤的参数")

    attachments: List[attachment] = Field(default_factory=list, description="测试或步骤的附件")

    # 步骤执行状态,通过，失败，跳过，未知，异常，运行中，完成·
    status: Literal['passed', 'failed', 'skipped', 'unknown', 'broken'] = Field(..., description="测试或步骤执行的状态。")

    statusDetails: Optional[StatusDetails] = Field(default=None, description="测试或步骤执行的详细状态信息。")

    # 测试或步骤的生命周期阶段，可能的值有：“scheduled”（已调度）、“running”（运行中）、“finished”（已完成）、“pending”（待处理）、“interrupted”（中断）
    stage: Literal['passed', 'scheduled', 'running', 'finished', 'pending', 'interrupted'] = Field(..., description="测试或步骤生命周期中的阶段。")

    # 步骤开始时间，Unix时间戳（毫秒）
    start: int
    # 步骤结束时间，Unix时间戳（毫秒）
    stop: int

    steps: List["Step"] = Field(default_factory=list, description="包含嵌套的步骤或子步骤")


class Execution(BaseModel):
    # 测试或步骤的执行状态
    status: str = Field(...,
                        description="测试或步骤完成时的状态。可能的值包括：'failed'、'broken'、'passed'、'skipped'、'unknown'。")

    # 状态详细信息，包括是否是已知的错误、是否是flaky测试等
    statusDetails: Optional[StatusDetails] = Field(default=None, description="测试或步骤执行的详细状态信息。")

    # 测试或步骤的生命周期阶段，可能的值有：“scheduled”（已调度）、“running”（运行中）、“finished”（已完成）、“pending”（待处理）、“interrupted”（中断）
    stage: Literal['passed', 'scheduled', 'running', 'finished', 'pending', 'interrupted'] = Field(..., description="测试或步骤生命周期中的阶段。")

    # 测试或步骤的开始时间（Unix时间戳，毫秒）
    start: int = Field(..., description="测试或步骤执行开始的时间，Unix时间戳格式。")

    # 测试或步骤的结束时间（Unix时间戳，毫秒）
    stop: int = Field(..., description="测试或步骤执行结束的时间，Unix时间戳格式。")

    # 包含嵌套的步骤或子步骤
    steps: List[Step] = Field(default_factory=list,
                              description="测试步骤的数组。每个步骤可以包含子步骤，表示嵌套的步骤和子步骤数组。")




class TestResult(Identifiers,MetaData,Execution):
    pass





