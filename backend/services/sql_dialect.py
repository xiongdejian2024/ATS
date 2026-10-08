"""Small SQL expressions whose text semantics differ between supported engines."""

from sqlalchemy import func


def text_tail(db, column, character_count):
    """Return the last Unicode characters without materializing the full value."""
    if db.get_bind().dialect.name == "postgresql":
        # PostgreSQL SUBSTR does not interpret a negative start from the end.
        return func.right(column, character_count)
    return func.substr(column, -character_count)


def text_position(db, haystack, needle):
    """Return a literal substring's one-based position, or zero if absent."""
    if db.get_bind().dialect.name == "postgresql":
        return func.strpos(haystack, needle)
    return func.instr(haystack, needle)
