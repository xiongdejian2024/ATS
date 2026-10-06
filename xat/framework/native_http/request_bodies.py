"""使用httpx原生multipart编码，保持参数/文件顺序和实际字节。"""

import hashlib
from .models import FrozenRequest


def references(request):
    if request.bodyType == "binary":
        return [request.binaryBody.file] if request.binaryBody.file else []
    return (
        [
            f
            for p in request.multipartParams
            if p.enable and p.paramType == "file"
            for f in p.files
        ]
        if request.bodyType == "multipart"
        else []
    )


async def load_files(request, loader):
    expected = {f.fileId: f for f in request.files}
    result = {}
    for ref in references(request):
        if ref.fileId in result:
            continue
        meta = expected.get(ref.fileId)
        if not meta or loader is None:
            raise ValueError("请求文件缺少冻结字节来源")
        content = await loader(meta)
        if (
            not isinstance(content, bytes)
            or len(content) != meta.byteLength
            or hashlib.sha256(content).hexdigest() != meta.sha256
        ):
            raise ValueError("实际请求文件大小或内容校验值与冻结版本不一致")
        result[ref.fileId] = content
    return result


def arguments(request, files):
    if request.bodyType == "binary":
        if not request.binaryBody.file:
            raise ValueError("二进制请求未选择实际文件")
        return dict(content=files[request.binaryBody.file.fileId])
    if request.bodyType != "multipart":
        return {}
    metadata = {f.fileId: f for f in request.files}
    parts = []
    for row in request.multipartParams:
        if not row.enable:
            continue
        if row.paramType == "file":
            parts.extend(
                (
                    row.key,
                    (
                        ref.fileAlias or metadata[ref.fileId].fileName,
                        files[ref.fileId],
                        metadata[ref.fileId].contentType,
                    ),
                )
                for ref in row.files
            )
        else:
            parts.append(
                (
                    row.key,
                    (
                        None,
                        row.value.encode("utf-8"),
                        "application/json" if row.paramType == "json" else None,
                    ),
                )
            )
    return dict(files=parts) if parts else {}
