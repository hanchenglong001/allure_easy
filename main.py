from datetime import datetime
import uuid as ud
from report_model import Identifiers, Link, Label,parameter,attachment,MetaData,StatusDetails,Step,Execution,TestResult


class Test_json():
    def __init__(self,name,historyid=None):
        self.name=name
        self.uuid=str(ud.uuid4())
        self.historyId=historyid
        self.testCaseId=str(ud.uuid4())
        # 创建 Identifiers 实例
        self.identifiers = Identifiers(
            uuid=self.uuid,
            historyId=self.historyId,
            testCaseId=self.testCaseId
        )


    def creat_report_json(self):
        return {
            **self.identifiers.model_dump(),
            **self.metadata.model_dump(),
            **self.execution.model_dump()
        }



# 示例数据
# 创建 Identifiers 实例
identifiers = Identifiers(
    uuid="9d95e6e7-9cf6-4ca5-91b4-9b69ce0971f8",
    historyId="2b35e31882061875031701ba05a3cd67",
    testCaseId="43f8868a367ff70177a99838d39c5b33"
)
# 创建 Link 实例
links = [
    Link(type="link", name="Allure Examples", url="https://examples.com/"),
    Link(type="issue", name="BUG-123", url="https://bugs.example.com/BUG-123")
]
# 创建 Label 实例
labels = [
    Label(name="host", value="machine-1"),
    Label(name="thread", value="306681-MainThread"),
    Label(name="language", value="java"),
    Label(name="framework", value="junit-platform"),
    Label(name="epic", value="Web interface"),
    Label(name="feature", value="Essential features"),
    Label(name="story", value="Authentication")
]
# 创建 Parameters 实例
parameters = [
    parameter(name="url", value="http://example.com/login")
]
# 创建 Attachments 实例
attachments = [
    attachment(name="Page Screenshot", source="67-attachment.png", type="png")
]

# 创建 MetaData 实例
metadata = MetaData(
    name="testAuthentication()",
    fullName="com.example.web.essentials.AuthenticationTest.testAuthentication",
    description="This test checks user authentication.",
    links=links,
    labels=labels,
    parameters=parameters,
    attachments=attachments
)

# 创建 StatusDetails 实例
status_details = StatusDetails(
    message="No issues"
)

# 创建 Step 实例
step1 = Step(
    name="Step 1: Open Login Page",
    parameters=[parameters[0]],
    attachments=[attachments[0]],
    status="passed",
    statusDetails=status_details,
    stage="finished",
    start=int(datetime.now().timestamp() * 1000),  # 当前时间戳（毫秒）
    stop=int(datetime.now().timestamp() * 1000),  # 当前时间戳（毫秒）
    steps=[]  # 无子步骤
)

# 创建 Execution 实例
execution = Execution(
    status="passed",
    statusDetails=status_details,
    stage="finished",
    start=int(datetime.now().timestamp() * 1000),  # 当前时间戳（毫秒）
    stop=int(datetime.now().timestamp() * 1000),  # 当前时间戳（毫秒）
    steps=[step1]  # 包含一个步骤
)

# 创建 Test_result 实例
test_result = TestResult(
  **execution.model_dump(),
  **metadata.model_dump(),
  **identifiers.model_dump()
)

# 输出 JSON 格式
print(test_result.model_dump_json(indent=4, ensure_ascii=False))  # `ensure_ascii=False` 以支持中文
