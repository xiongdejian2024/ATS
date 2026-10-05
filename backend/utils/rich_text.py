"""判断富文本是否包含可见内容，避免空段落绕过必填约束。"""

from html.parser import HTMLParser
import re


class VisibleContent(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden_depth = 0
        self.parts = []
        self.image = False

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "template"}:
            self.hidden_depth += 1
        if not self.hidden_depth and tag == "img":
            self.image |= any(
                key == "src" and value and value.strip() for key, value in attrs
            )

    def handle_endtag(self, tag):
        if tag in {"script", "style", "template"} and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data):
        if not self.hidden_depth:
            self.parts.append(data)


def has_visible_content(value):
    # 历史纯文本可以含比较符号，只有实际HTML标签才按富文本解析。
    if not re.search(r"</?[a-zA-Z][\s\S]*>", value):
        return bool(value.replace("\u200b", "").replace("\ufeff", "").strip())
    parser = VisibleContent()
    parser.feed(value)
    text = "".join(parser.parts).replace("\u200b", "").replace("\ufeff", "")
    return bool(parser.image or text.strip())
