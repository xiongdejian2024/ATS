"""功能脑图当前范围与执行参数；复用已有严格实例选择规则。"""
from uuid import UUID
from typing import Literal
from pydantic import Field
from schemas.plan_native_selection import NativeWorkspaceSelection


class FunctionalMinderSelection(NativeWorkspaceSelection):
    category: Literal['functional'] = 'functional'


class FunctionalMinderExecute(FunctionalMinderSelection):
    requestId: UUID
    result: Literal['pending', 'passed', 'failed', 'blocked']
    description: str = Field('', max_length=20000)

    @property
    def stepResults(self):
        # 脑图整体/目录回填不伪造逐步骤结果；步骤弹窗走原单用例执行入口。
        return []
