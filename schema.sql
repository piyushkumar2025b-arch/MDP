-- 🧬 CHEMOFILTER v1M OMNIPOTENT REGISTRY (Cloudflare D1)
-- FINAL VANGUARD 2026 EDITION
-- Lead Molecule Registry
CREATE TABLE IF NOT EXISTS molecules (
    cid TEXT PRIMARY KEY,
    smiles TEXT NOT NULL,
    lead_score REAL DEFAULT 0,
    grade TEXT DEFAULT 'N/A',
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
-- Advanced Aether-Primality Analytics (v10k - v1M)
CREATE TABLE IF NOT EXISTS aether_vault (
    molecule_id TEXT,
    aether_score REAL,
    quantum_flux REAL,
    evolution_path TEXT,
    -- JSON Object
    multiverse_id TEXT,
    genetic_risk_index TEXT,
    FOREIGN KEY(molecule_id) REFERENCES molecules(cid)
);
-- IP & Novelty Scouting Records
CREATE TABLE IF NOT EXISTS ip_registry (
    molecule_id TEXT,
    novelty_index REAL,
    fto_status TEXT,
    patent_overlap_hits INTEGER,
    last_scanned DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(molecule_id) REFERENCES molecules(cid)
);
-- Research & Integrity Vault Logs
CREATE TABLE IF NOT EXISTS integrity_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT,
    compound_id TEXT,
    verification_hash TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);