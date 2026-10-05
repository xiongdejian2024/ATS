"""批量读取原生配置和最近真实执行记录，不用通用用例状态代替。"""
from models import TestCase, TestExecution
from models.test_suite import TestSuiteExecution
from models.native_case import ApiDefinition, ApiTestEnvironment, NativeCaseConfig
from services.native_case import fingerprint
from services.filter_values import temporal

NATIVE_FIELDS = {'nativeState', 'protocol', 'path', 'apiChange', 'environmentName', 'lastReportStatus', 'stepTotal'}


class NativeCandidateContext:
    def __init__(self, db, project_id):
        self.configs = {row.case_id: row for row in db.query(NativeCaseConfig).join(TestCase, TestCase.id == NativeCaseConfig.case_id).filter(TestCase.project_id == project_id)}
        self.definitions = {r.id: r for r in db.query(ApiDefinition).filter_by(project_id=project_id)}
        self.environments = {r.id: r for r in db.query(ApiTestEnvironment).filter_by(project_id=project_id)}
        records = {}
        for model in [TestExecution, TestSuiteExecution]:
            for row in db.query(model.id, model.case_id, model.result, model.executed_at).join(TestCase, TestCase.id == model.case_id).filter(TestCase.project_id == project_id):
                records.setdefault(row.id, row)
        self.latest = {}
        for row in sorted(records.values(), key=lambda r: (temporal(r.executed_at), r.id), reverse=True):
            self.latest.setdefault(row.case_id, row)

    def values(self, case):
        row = self.configs.get(case.id)
        definition = self.definitions.get(row.api_definition_id) if row else None
        environment = self.environments.get(row.environment_id) if row else None
        record = self.latest.get(case.id)
        report = record.result if record else None
        report = {'passed': 'SUCCESS', 'pass': 'SUCCESS', 'failed': 'ERROR', 'fail': 'ERROR', 'error': 'ERROR', 'fake_error': 'FAKE_ERROR'}.get(report, report)
        return dict(nativeState=row.state if row else None,
                    protocol=definition.protocol if definition else None,
                    path=definition.path if definition else None,
                    apiChange=(row.definition_fingerprint != fingerprint(definition.parameters)) if definition and row else None,
                    environmentName=environment.id if environment else None,
                    environmentLabel=environment.name if environment else None,
                    lastReportStatus=report,
                    stepTotal=len(case.steps or []) if case.type == 'scenario' else None)
