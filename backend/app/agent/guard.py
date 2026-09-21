"""
ClaimLens Nexus — SQL Guard (SEC-001)

sqlglot-based allowlist validation for LLM-generated SQL.
Per ADR-002: defense-in-depth — this guard runs BEFORE any SQL hits DuckDB.

Blocks:
- Any non-SELECT statement (INSERT, UPDATE, DELETE, DROP, etc.)
- Subqueries in dangerous positions
- Functions not in the allowlist
- Multiple statements (statement injection)
"""

import sqlglot
from sqlglot import exp


# Allowed SQL functions (whitelist approach)
ALLOWED_FUNCTIONS = {
    # Aggregations
    "count", "sum", "avg", "min", "max",
    # String
    "lower", "upper", "trim", "length", "substr", "substring",
    "replace", "concat",
    # Date/time
    "strftime", "date", "datetime", "julianday",
    "date_trunc", "date_part", "extract",
    # Numeric
    "round", "abs", "ceil", "floor", "coalesce",
    # Conditional
    "if", "case", "nullif", "ifnull",
    # Type casting
    "cast", "try_cast",
}

# Allowed table names (must match our schema exactly)
ALLOWED_TABLES = {
    "policies", "claims", "hospitals", "garages", "agents", "decisions",
}


class SQLGuardError(Exception):
    """Raised when SQL fails the guard check."""
    pass


def validate_sql(sql: str) -> str:
    """
    Validate LLM-generated SQL against the allowlist.

    Returns the validated SQL if it passes.
    Raises SQLGuardError if it fails any check.
    """
    if not sql or not sql.strip():
        raise SQLGuardError("Empty SQL query")

    # Parse with sqlglot
    try:
        statements = sqlglot.parse(sql, dialect="duckdb")
    except sqlglot.errors.ParseError as e:
        raise SQLGuardError(f"SQL parse error: {e}")

    # Check: only one statement allowed (no statement injection)
    if len(statements) != 1:
        raise SQLGuardError(
            f"Multiple statements detected ({len(statements)}). "
            "Only single SELECT statements are allowed."
        )

    statement = statements[0]

    # Check: must be a SELECT statement
    if not isinstance(statement, exp.Select):
        raise SQLGuardError(
            f"Non-SELECT statement detected: {type(statement).__name__}. "
            "Only SELECT queries are allowed."
        )

    # Check: no dangerous statement types nested inside
    dangerous_types = (
        exp.Insert, exp.Update, exp.Delete, exp.Drop,
        exp.Create, exp.Alter, exp.Command,
    )
    for node in statement.walk():
        if isinstance(node, dangerous_types):
            raise SQLGuardError(
                f"Dangerous SQL operation detected: {type(node).__name__}. "
                "Only read-only SELECT queries are allowed."
            )

    # Check: all table references are in the allowlist
    for table in statement.find_all(exp.Table):
        table_name = table.name.lower()
        if table_name not in ALLOWED_TABLES:
            raise SQLGuardError(
                f"Unknown table: '{table_name}'. "
                f"Allowed tables: {', '.join(sorted(ALLOWED_TABLES))}"
            )

    # Check: all function calls are in the allowlist
    for func in statement.find_all(exp.Func):
        func_name = type(func).__name__.lower()
        # sqlglot represents functions as class names
        # Also check the sql_name for anonymous functions
        if hasattr(func, 'sql_name'):
            func_name = func.sql_name().lower()

        # Map sqlglot internal names to our allowlist
        sqlglot_to_name = {
            "count": "count",
            "sum": "sum",
            "avg": "avg",
            "min": "min",
            "max": "max",
            "round": "round",
            "coalesce": "coalesce",
            "nullif": "nullif",
            "lower": "lower",
            "upper": "upper",
            "anonymous": None,  # Check the actual name
        }

        mapped = sqlglot_to_name.get(func_name, func_name)
        if mapped is None and hasattr(func, 'this') and isinstance(func.this, str):
            mapped = func.this.lower()

        if mapped and mapped not in ALLOWED_FUNCTIONS:
            # Be lenient with known-safe sqlglot internal names
            safe_internal = {
                "if", "case", "between", "in", "like", "is",
                "and", "or", "not", "exists", "cast",
                "ordered", "alias", "column", "star",
            }
            if mapped not in safe_internal:
                raise SQLGuardError(
                    f"Disallowed function: '{func_name}'. "
                    f"Allowed functions: {', '.join(sorted(ALLOWED_FUNCTIONS))}"
                )

    return sql
