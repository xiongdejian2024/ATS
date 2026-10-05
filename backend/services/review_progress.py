"""评审生命周期及进度；有效结论和整单完成状态分开计算。"""

from decimal import Decimal, ROUND_HALF_UP


def pass_rate(passed, total):
    if not total:
        return 0
    # 官方先按比例保留两位小数，再转为百分数；1/3显示33%，1/8显示13%。
    ratio = (Decimal(passed) / Decimal(total)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    return int(ratio * 100)


def metrics(items, *, archived=False, status="pending", started=False):
    total = len(items)
    passed = sum(item["status"] == "approved" for item in items)
    rejected = sum(item["status"] == "rejected" for item in items)
    rereview = sum(item["status"] == "re_review" for item in items)
    reviewing = sum(
        item["status"] == "pending"
        and any(
            d["decision"] == "approved"
            and ("reviewerIds" not in item or d["reviewerId"] in item["reviewerIds"])
            for d in item.get("decisions", [])
        )
        for item in items
    )
    return count_metrics(
        total,
        passed,
        rejected,
        rereview,
        reviewing,
        archived=archived,
        status=status,
        started=started,
    )


def count_metrics(
    total,
    passed,
    rejected,
    rereview,
    reviewing,
    *,
    archived=False,
    status="pending",
    started=False,
):
    reviewed = passed + rejected
    if archived:
        lifecycle = "archived"
    elif status in {"cancelled", "superseded"}:
        lifecycle = status
    elif reviewed + rereview + reviewing == 0:
        lifecycle = "prepared"
    elif reviewed == total:
        lifecycle = "completed"
    else:
        lifecycle = "underway"
    return dict(
        lifecycle=lifecycle,
        caseCount=total,
        passCount=passed,
        unPassCount=rejected,
        reReviewedCount=rereview,
        underReviewedCount=reviewing,
        unReviewCount=total - reviewed - rereview - reviewing,
        reviewedCount=reviewed,
        # 使用与官方浏览器相同的IEEE浮点结果，再按toFixed(2)规则舍入。
        progress=(
            float(
                Decimal.from_float(reviewed / total * 100).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
            )
            if total
            else 0
        ),
        passRate=pass_rate(passed, total),
    )
