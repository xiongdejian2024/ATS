"""计划关联候选范围；分页和身份由服务端决定。"""
from typing import Any, Literal
from pydantic import Field, StrictBool, field_validator, model_validator
from schemas.case_selection import ScopeRequest

Category = Literal['functional', 'api', 'scenario']


class CandidateCondition(ScopeRequest):
    search: str = Field('', max_length=255)
    folder: str = Field('all', min_length=1, max_length=36)
    priority: Literal['P0', 'P1', 'P2', 'P3'] | None = None
    filters: dict[str, Any] | None = None
    mine: StrictBool = False
    protocols: list[str] | None = Field(None, max_length=100)
    methods: list[str] = Field(default_factory=list, max_length=100)
    createdBy: list[str] = Field(default_factory=list, max_length=100)

    @field_validator('protocols', 'methods', 'createdBy')
    @classmethod
    def basic_values(cls, values):
        if values is not None and (len(values) != len(set(values)) or any(not value.strip() or value != value.strip() or len(value) > 50 for value in values)):
            raise ValueError('基础筛选项须为不重复的1到50字符文本')
        return values


class CandidateModuleSelection(ScopeRequest):
    selectAll: StrictBool = False
    selectIds: list[str] = Field(default_factory=list, max_length=10000)
    excludeIds: list[str] = Field(default_factory=list, max_length=10000)

    @field_validator('selectIds', 'excludeIds')
    @classmethod
    def unique_ids(cls, values):
        if any(not value.strip() or value != value.strip() or len(value) > 36 for value in values):
            raise ValueError('用例ID须为1到36字符且不含首尾空白')
        if len(values) != len(set(values)):
            raise ValueError('用例ID不能重复')
        return values

    @model_validator(mode='after')
    def mode(self):
        if self.selectAll and self.selectIds or not self.selectAll and self.excludeIds:
            raise ValueError('模块全选与逐条选择不能混用')
        return self


class CandidateSelection(ScopeRequest):
    projectId: str | None = Field(None, min_length=1, max_length=36)
    category: Category = 'functional'
    resourceType: Literal['CASE', 'API'] = 'CASE'
    selectAll: StrictBool = False
    caseIds: list[str] = Field(default_factory=list, max_length=10000)
    definitionIds: list[str] = Field(default_factory=list, max_length=10000)
    excludeIds: list[str] = Field(default_factory=list, max_length=10000)
    condition: CandidateCondition = Field(default_factory=CandidateCondition)
    moduleMaps: dict[str, CandidateModuleSelection] | None = None
    syncCase: StrictBool = False
    apiCaseCollectionId: str | None = Field(None, min_length=1, max_length=36)
    apiScenarioCollectionId: str | None = Field(None, min_length=1, max_length=36)

    @field_validator('caseIds', 'definitionIds', 'excludeIds')
    @classmethod
    def unique_ids(cls, values):
        if any(not value.strip() or value != value.strip() or len(value) > 36 for value in values):
            raise ValueError('用例ID须为1到36字符且不含首尾空白')
        if len(values) != len(set(values)):
            raise ValueError('用例ID不能重复')
        return values

    @model_validator(mode='after')
    def selection_mode(self):
        if self.resourceType == 'API' and (self.category != 'api' or self.caseIds):
            raise ValueError('接口模式仅用于API分类，须提交接口ID而非用例ID')
        if self.resourceType == 'CASE' and self.definitionIds:
            raise ValueError('用例模式不能提交接口ID')
        selected_ids = self.definitionIds if self.resourceType == 'API' else self.caseIds
        basic = self.condition.protocols is not None or bool(self.condition.methods) or bool(self.condition.createdBy)
        if basic and self.category != 'api':
            raise ValueError('协议与接口列筛选只适用于API分类')
        if self.condition.methods and self.resourceType != 'API':
            raise ValueError('请求方式列筛选只适用于接口模式')
        if basic and (self.condition.filters is not None or self.condition.mine):
            raise ValueError('高级视图不能混用接口基础筛选')
        if self.syncCase and self.category != 'functional':
            raise ValueError('只有功能用例支持同步关联用例')
        if not self.syncCase and (self.apiCaseCollectionId or self.apiScenarioCollectionId):
            raise ValueError('请先开启同步关联用例')
        if self.moduleMaps is not None:
            if not self.moduleMaps or len(self.moduleMaps) > 10000:
                raise ValueError('请选择1到10000个模块范围')
            if self.selectAll or selected_ids or self.excludeIds:
                raise ValueError('模块选择不能混用旧选择范围')
            if self.condition.folder != 'all' or self.condition.filters is not None or self.condition.mine:
                raise ValueError('模块组合仅支持全目录基础筛选')
            if any(not key.strip() or key != key.strip() or len(key) > 36 for key in self.moduleMaps):
                raise ValueError('模块ID须为1到36字符且不含首尾空白')
            if 'all' in self.moduleMaps and not self.moduleMaps['all'].selectAll:
                raise ValueError('全部模块入口只能全选')
            ids = [value for entry in self.moduleMaps.values() for value in entry.selectIds + entry.excludeIds]
            if len(ids) > 10000 or len(set(ids)) != len(ids):
                raise ValueError('模块用例ID不能重复且总数不能超过10000')
        elif self.selectAll:
            if selected_ids:
                raise ValueError('范围全选不能混用逐条用例ID')
            from fastapi import HTTPException
            from services.plan_candidate_filter import parse_candidate_filters
            try:
                if self.resourceType == 'API':
                    from services.plan_definition_candidates import parse_definition_filters
                    parse_definition_filters(self.condition.filters)
                else:
                    parse_candidate_filters(self.condition.filters, self.category)
            except HTTPException as exc:
                from core.logger import logger
                logger.exception('计划关联范围高级筛选校验失败')
                raise ValueError(exc.detail) from exc
        elif not selected_ids or self.excludeIds or self.condition.model_fields_set - {'protocols', 'methods', 'createdBy'}:
            raise ValueError('逐条选择必须指定ID，不能混用筛选条件或排除项')
        return self


class Association(CandidateSelection):
    collectionId: str | None = Field(None, min_length=1, max_length=36)
    suiteId: str | None = Field(None, min_length=1, max_length=36)
    syncApiSuiteId: str | None = Field(None, min_length=1, max_length=36)
    syncScenarioSuiteId: str | None = Field(None, min_length=1, max_length=36)
