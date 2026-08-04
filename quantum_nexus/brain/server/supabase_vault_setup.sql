-- Run this in Supabase SQL Editor (Dashboard → SQL)
-- Creates encrypted secrets vault with RLS

CREATE TABLE IF NOT EXISTS secrets_vault (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  service TEXT NOT NULL UNIQUE,
  key_name TEXT NOT NULL,
  key_value TEXT NOT NULL,
  category TEXT DEFAULT 'general',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS: Only service role can access
ALTER TABLE secrets_vault ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role full access" ON secrets_vault
  FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Anon no access" ON secrets_vault
  FOR ALL USING (false);

-- Index for fast lookups
CREATE INDEX idx_secrets_vault_service ON secrets_vault(service);
CREATE INDEX idx_secrets_vault_category ON secrets_vault(category);

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER secrets_vault_updated_at
  BEFORE UPDATE ON secrets_vault
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
