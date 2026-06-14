import sqlite3
from pathlib import Path


class LeadsDatabase:
    def __init__(self, db_path: str = "data/leads.db"):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS leads (
                id                   INTEGER PRIMARY KEY AUTOINCREMENT,
                domain               TEXT UNIQUE NOT NULL,
                company_name         TEXT,
                description          TEXT,
                industry             TEXT,
                location             TEXT,
                website              TEXT,
                email                TEXT,
                phone                TEXT,
                linkedin             TEXT,
                employees            TEXT,
                legitimacy_score     INTEGER DEFAULT 0,
                legitimacy_reason    TEXT,
                company_type         TEXT,
                recommended_approach TEXT,
                positive_indicators  TEXT,
                red_flags            TEXT,
                search_query         TEXT,
                scraped_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS scrape_sessions (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                service_description TEXT,
                target_industry     TEXT,
                location            TEXT,
                total_found         INTEGER DEFAULT 0,
                total_qualified     INTEGER DEFAULT 0,
                started_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at        TIMESTAMP
            );
        """)
        self.conn.commit()

    def is_scraped(self, domain: str) -> bool:
        cur = self.conn.execute("SELECT 1 FROM leads WHERE domain = ?", (domain,))
        return cur.fetchone() is not None

    def save_lead(self, lead: dict) -> bool:
        try:
            self.conn.execute(
                """
                INSERT INTO leads (
                    domain, company_name, description, industry, location, website,
                    email, phone, linkedin, employees, legitimacy_score, legitimacy_reason,
                    company_type, recommended_approach, positive_indicators, red_flags, search_query
                ) VALUES (
                    :domain, :company_name, :description, :industry, :location, :website,
                    :email, :phone, :linkedin, :employees, :legitimacy_score, :legitimacy_reason,
                    :company_type, :recommended_approach, :positive_indicators, :red_flags, :search_query
                )
                """,
                lead,
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_leads(self, min_score: int = 0) -> list:
        cur = self.conn.execute(
            "SELECT * FROM leads WHERE legitimacy_score >= ? ORDER BY legitimacy_score DESC",
            (min_score,),
        )
        return [dict(row) for row in cur.fetchall()]

    def get_stats(self) -> dict:
        cur = self.conn.execute(
            "SELECT COUNT(*), AVG(legitimacy_score), MAX(legitimacy_score) FROM leads"
        )
        row = cur.fetchone()
        return {
            "total": row[0],
            "avg_score": round(row[1] or 0, 1),
            "max_score": row[2] or 0,
        }

    def start_session(self, service_description: str, target_industry: str, location: str) -> int:
        cur = self.conn.execute(
            "INSERT INTO scrape_sessions (service_description, target_industry, location) VALUES (?, ?, ?)",
            (service_description, target_industry, location),
        )
        self.conn.commit()
        return cur.lastrowid

    def complete_session(self, session_id: int, total_found: int, total_qualified: int):
        self.conn.execute(
            """UPDATE scrape_sessions
               SET total_found=?, total_qualified=?, completed_at=CURRENT_TIMESTAMP
               WHERE id=?""",
            (total_found, total_qualified, session_id),
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
