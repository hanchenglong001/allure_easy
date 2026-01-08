import json
import os
import warnings
from datetime import datetime
import uuid as ud
from typing import List

from report_model import Identifiers, Link, Label,parameter,attachment,MetaData,StatusDetails,Step,Execution,TestResult


class Test_Case:
    def __init__(self,name,historyid=None):
        self.name=name
        self.uuid=str(ud.uuid4())
        if historyid:
            self.historyId=historyid
        else:
            self.historyId=str(ud.uuid4())
        self.testCaseId=str(ud.uuid4())
        # 创建 Identifiers 实例
        self.identifiers = Identifiers(
            uuid=self.uuid,
            historyId=self.historyId,
            testCaseId=self.testCaseId
        )
        self.metadata=None
        self.execution=None
        self.links=[]
        self.labels=[]
        self.cparameters=[]
        self.cattachments=[]

    def add_links(self,link: Link):
        if self.metadata:
            raise "用例已经创建无法添加"
        self.links.append(link)

    def add_label(self,label: Label):
        if self.metadata:
            raise "用例已经创建无法添加"
        self.labels.append(label)

    def add_case_parameters(self, parameter:parameter):
        if self.metadata:
            raise "用例已经创建无法添加"
        self.cparameters.append(parameter)

    def add_case_attachments(self, attachment: attachment):
        if self.metadata:
            raise "用例已经创建无法添加"
        self.cattachments.append(attachment)

    def create_case(self,name,fullName,description,status,status_details:StatusDetails,stage,start_time:datetime,stop_time:datetime,steps:List[Step]= []):
        """

        :param steps: 步骤数组
        :param stop_time: 测试用例的结束时间
        :param start_time: 测试用例的开始时间
        :param name: 测试用例名称
        :param fullName: 测试用例的完整名称
        :param description: 测试用例的描述
        :param status:  测试用例的执行状态     passed,broken,passed,skipped,unknown
        :param status_details: 测试用例的详细状态信息
        :param stage: 测试用例的生命周期阶段  scheduled,running,finished,pending,interrupted
        :return:
        """
        checks = [
            (self.links, "用例links为空"),
            (self.labels, "用例labels为空"),
            (self.cparameters, "用例parameters为空"),
            (self.cattachments, "用例attachments为空")
        ]
        for field, warning_msg in checks:
            if not field:
                warnings.warn(warning_msg)

        self.metadata = MetaData(
            name=name,
            fullName=fullName,
            description=description,
            links=self.links,
            labels=self.labels,
            parameters=self.cparameters,
            attachments=self.cattachments
        )
        self.execution=Execution(
            status=status,
            statusDetails=status_details,
            stage=stage,
            start=int(start_time.timestamp() * 1000),  # 当前时间戳（毫秒）
            stop=int(stop_time.timestamp() * 1000),  # 当前时间戳（毫秒）
            steps=steps  # 包含一个步骤
        )
        return {
            **self.identifiers.model_dump(),
            **self.metadata.model_dump(),
            **self.execution.model_dump()
        }


    def create_step(self,name,status,status_details:StatusDetails,stage,start_time:datetime,stop_time:datetime,steps:List[Step]= [],parameters:List[parameter]= [],attachments:List[attachment]= []):
        """

        :param name: 步骤名称
        :param status: 步骤执行状态 passed,broken,passed,skipped,unknown
        :param status_details: 步骤的详细状态信息
        :param stage: 步骤生命周期阶段  scheduled,running,finished,pending,interrupted
        :param parameters: 步骤的参数
        :param attachments: 步骤的附件
        :param start_time: 步骤开始时间
        :param stop_time: 步骤结束时间
        :param steps: 子步骤
        :return:
        """
        return Step(
            name=name,
            parameters=parameters,
            attachments=attachments,
            status=status,
            statusDetails=status_details,
            stage=stage,
            start=int(start_time.timestamp() * 1000),  # 当前时间戳（毫秒）
            stop=int(stop_time.timestamp() * 1000),  # 当前时间戳（毫秒）
            steps=steps # 无子步骤
        )

def main():
    # 创建 StatusDetails 实例
    tc = Test_Case("测试一下")
    tc.add_links(Link(type="link", name="Allure Examples", url="https://examples.com/"))
    tc.add_links(Link(type="link", name="Allure Examples", url="https://examples.com/"))
    tc.add_label(Label(name="framework", value="pytest"))
    tc.add_case_parameters(parameter(name="url", value="http://example.com/login"))
    tc.add_case_attachments(attachment(name="Page Screenshot", source="67-attachment.png", type="png"))
    status_details = StatusDetails(message="No issues")
    step1 = tc.create_step("测试一下step", "passed", status_details, "scheduled", datetime.now(), datetime.now())
    case = tc.create_case("测试case", "完全名字", "描述一下啊", "passed", status_details, "scheduled", datetime.now(),
                          datetime.now(), [step1])
    with open(f"allure-results/{case['uuid']}-result.json", "w", encoding="utf-8") as f:
        json.dump(case, f, ensure_ascii=False)


if __name__ == '__main__':
    for i in range(10000):
        print(i)
        main()
    ##删除临时文件
    os.system("del /s /q allure-report")
    os.system("allure generate ")
    os.system("allure open ")



