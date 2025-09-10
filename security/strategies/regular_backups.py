# strategies/regular_backups.py
from __future__ import annotations
from typing import List, Dict
from .overview import Strategy


class RegularBackups(Strategy):
    """
    Essential Eight – Regular Backups
    Detects whether backups are configured, working, and tested.
    Checks evidence such as backup logs, configuration exports,
    restore test results, and related screenshots/text.
    """

    id = "RB01"
    name = "Regular Backups"

    def description(self) -> str:
        return (
            "Checks backup schedule, offsite/immutable copies, encryption, "
            "recent backup success, restore test results, retention, and access controls."
        )

    @staticmethod
    def _row(
        tid: str,
        sub: str,
        lvl: str,
        pf: str,
        prio: str,
        rec: str,
        ev: List[str]
    ) -> Dict:
        return {
            "test_id": tid,
            "sub_strategy": sub,
            "detected_level": lvl,
            "pass_fail": pf,
            "priority": prio,
            "recommendation": rec,
            "evidence": ev,
        }

    def emit_hits(self, text: str, source_file: str = "") -> List[Dict]:
        rows: List[Dict] = []
        t = (text or "").lower()

        # === ML1-RB-01: Backups configured & recent ===
        if "backup completed successfully" in t or "last backup" in t:
            rows.append(self._row(
                "ML1-RB-01", "Backups are configured and recent", "ML1", "PASS", "High",
                "Ensure backups continue to run successfully on schedule.",
                [source_file]
            ))
        elif "backup failed" in t or "no recent backup" in t:
            rows.append(self._row(
                "ML1-RB-01", "Backups are configured and recent", "ML1", "FAIL", "High",
                "Fix failed backups and verify backup scheduling.",
                [source_file]
            ))

        # === ML1-RB-02: Offsite or immutable ===
        if "offsite" in t or "cloud backup" in t or "immutable" in t:
            rows.append(self._row(
                "ML1-RB-02", "Backups stored offsite/immutable", "ML1", "PASS", "Medium",
                "Maintain offsite/immutable copies to prevent ransomware impact.",
                [source_file]
            ))

        # === ML1-RB-03: Restore tested ===
        if "restore test successful" in t or "backup restored" in t:
            rows.append(self._row(
                "ML1-RB-03", "Restore process tested", "ML1", "PASS", "Medium",
                "Regularly test restoring backups to validate integrity.",
                [source_file]
            ))
        elif "restore failed" in t:
            rows.append(self._row(
                "ML1-RB-03", "Restore process tested", "ML1", "FAIL", "High",
                "Investigate and fix restore test issues immediately.",
                [source_file]
            ))

        # === ML1-RB-04: Retention policy ===
        if "retention policy" in t or "kept for" in t:
            rows.append(self._row(
                "ML1-RB-04", "Retention policy in place", "ML1", "PASS", "Low",
                "Ensure backups are retained per compliance requirements.",
                [source_file]
            ))

        # === ML1-RB-05: Encrypted backups ===
        if "encrypted backup" in t or "aes" in t or "rsa" in t:
            rows.append(self._row(
                "ML1-RB-05", "Backups encrypted", "ML1", "PASS", "High",
                "Use strong encryption to protect backup data.",
                [source_file]
            ))

        # === ML1-RB-06: Access controlled ===
        if "restricted access" in t or "admin only" in t:
            rows.append(self._row(
                "ML1-RB-06", "Backups access controlled", "ML1", "PASS", "Medium",
                "Restrict access to backups only to authorized personnel.",
                [source_file]
            ))

        return rows


def get_strategy():
    return RegularBackups()
