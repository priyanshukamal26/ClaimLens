"""
ClaimLens Nexus — SQL Guard Hostile Test Suite (SEC-001)

25-case hostile SQL injection test suite per ADR-002 and REQUIREMENTS.md SEC-001.
Validates that the sqlglot-based allowlist guard blocks every known attack vector
while passing legitimate analytical queries without false positives.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.agent.guard import validate_sql, SQLGuardError


# ============================================================
# PART A: 25 Hostile SQL Injection Test Cases (must ALL be rejected)
# ============================================================

class TestHostileSQLInjection:
    """Each test verifies that a specific attack vector is blocked by the guard."""

    def test_01_drop_table(self):
        with pytest.raises(SQLGuardError):
            validate_sql("DROP TABLE claims")

    def test_02_stacked_statements(self):
        with pytest.raises(SQLGuardError):
            validate_sql("SELECT * FROM policies; DROP TABLE claims")

    def test_03_insert(self):
        with pytest.raises(SQLGuardError):
            validate_sql("INSERT INTO claims (claim_id) VALUES ('FAKE-001')")

    def test_04_update(self):
        with pytest.raises(SQLGuardError):
            validate_sql("UPDATE claims SET anomaly_score = 0 WHERE claim_id = 'CLM-001'")

    def test_05_delete(self):
        with pytest.raises(SQLGuardError):
            validate_sql("DELETE FROM claims WHERE claim_id = 'CLM-001'")

    def test_06_create_table(self):
        with pytest.raises(SQLGuardError):
            validate_sql("CREATE TABLE exfil AS SELECT * FROM claims")

    def test_07_alter_table(self):
        with pytest.raises(SQLGuardError):
            validate_sql("ALTER TABLE claims ADD COLUMN backdoor TEXT")

    def test_08_attach_database(self):
        with pytest.raises(SQLGuardError):
            validate_sql("ATTACH DATABASE '/tmp/evil.db' AS evil")

    def test_09_detach_database(self):
        with pytest.raises(SQLGuardError):
            validate_sql("DETACH DATABASE main")

    def test_10_pragma(self):
        with pytest.raises(SQLGuardError):
            validate_sql("PRAGMA table_info(claims)")

    def test_11_system_function(self):
        with pytest.raises(SQLGuardError):
            validate_sql("SELECT system('cat /etc/passwd')")

    def test_12_read_csv(self):
        with pytest.raises(SQLGuardError):
            validate_sql("SELECT * FROM read_csv('/etc/passwd')")

    def test_13_install_extension(self):
        with pytest.raises(SQLGuardError):
            validate_sql("INSTALL httpfs")

    def test_14_sqlite_master(self):
        with pytest.raises(SQLGuardError):
            validate_sql("SELECT * FROM sqlite_master")

    def test_15_arbitrary_table(self):
        with pytest.raises(SQLGuardError):
            validate_sql("SELECT * FROM users WHERE password = 'admin'")

    def test_16_dangerous_function_sleep(self):
        with pytest.raises(SQLGuardError):
            validate_sql("SELECT sleep(10) FROM policies")

    def test_17_subquery_mutation(self):
        with pytest.raises(SQLGuardError):
            validate_sql("SELECT * FROM policies; UPDATE claims SET anomaly_score = 0")

    def test_18_comment_injection(self):
        with pytest.raises(SQLGuardError):
            validate_sql("SELECT * FROM policies; -- innocent comment\nDROP TABLE claims")

    def test_19_multiple_semicolons(self):
        with pytest.raises(SQLGuardError):
            validate_sql("SELECT 1; SELECT 2; SELECT 3")

    def test_20_malformed_sql(self):
        with pytest.raises(SQLGuardError):
            validate_sql("SELECCT * FORM policies WHER 1=1")

    def test_21_empty_query(self):
        with pytest.raises(SQLGuardError):
            validate_sql("")

    def test_22_whitespace_only(self):
        with pytest.raises(SQLGuardError):
            validate_sql("   \n\t  ")

    def test_23_disallowed_function_pg_sleep(self):
        with pytest.raises(SQLGuardError):
            validate_sql("SELECT pg_sleep(10) FROM policies")

    def test_24_copy_to(self):
        with pytest.raises(SQLGuardError):
            validate_sql("COPY claims TO '/tmp/exfil.csv'")

    def test_25_set_config(self):
        with pytest.raises(SQLGuardError):
            validate_sql("SET enable_external_access = true")


# ============================================================
# PART B: Legitimate Queries (must ALL pass — zero false positives)
# ============================================================

class TestLegitimateQueries:
    """Validate that the guard does NOT block valid analytical queries."""

    def test_valid_simple_select(self):
        sql = "SELECT COUNT(*) FROM claims"
        assert validate_sql(sql) == sql

    def test_valid_join_query(self):
        sql = """
            SELECT p.state, COUNT(c.claim_id) as claims_count
            FROM claims c
            JOIN policies p ON c.policy_id = p.policy_id
            GROUP BY p.state
            ORDER BY claims_count DESC
            LIMIT 10
        """
        result = validate_sql(sql)
        assert result == sql

    def test_valid_aggregation(self):
        sql = """
            SELECT
                p.line_of_business,
                ROUND(SUM(c.claim_amount) / NULLIF(SUM(p.premium_amount), 0) * 100, 2) as loss_ratio
            FROM claims c
            JOIN policies p ON c.policy_id = p.policy_id
            GROUP BY p.line_of_business
        """
        result = validate_sql(sql)
        assert result == sql

    def test_valid_where_clause(self):
        sql = "SELECT * FROM claims WHERE anomaly_score > 0.3 ORDER BY anomaly_score DESC LIMIT 20"
        assert validate_sql(sql) == sql

    def test_valid_multi_table_join(self):
        sql = """
            SELECT c.claim_id, p.policyholder_name, h.name as hospital_name
            FROM claims c
            JOIN policies p ON c.policy_id = p.policy_id
            LEFT JOIN hospitals h ON c.hospital_id = h.hospital_id
            WHERE c.anomaly_score > 0.3
        """
        result = validate_sql(sql)
        assert result == sql

    def test_valid_substr_date_grouping(self):
        sql = """
            SELECT substr(c.claim_date, 1, 7) as month, COUNT(*) as count
            FROM claims c
            GROUP BY substr(c.claim_date, 1, 7)
            ORDER BY month
        """
        result = validate_sql(sql)
        assert result == sql

    def test_valid_case_when(self):
        sql = """
            SELECT
                COUNT(CASE WHEN status = 'Approved' THEN 1 END) as approved,
                COUNT(CASE WHEN status = 'Pending' THEN 1 END) as pending
            FROM claims
        """
        result = validate_sql(sql)
        assert result == sql

    def test_valid_coalesce(self):
        sql = "SELECT COALESCE(settlement_amount, 0) FROM claims LIMIT 5"
        assert validate_sql(sql) == sql

    def test_valid_all_allowed_tables(self):
        """Verify all 6 allowed tables are individually accessible."""
        for table in ["policies", "claims", "hospitals", "garages", "agents", "decisions"]:
            sql = f"SELECT COUNT(*) FROM {table}"
            assert validate_sql(sql) == sql
