CREATE TABLE IF NOT EXISTS symbols (
  symbol TEXT PRIMARY KEY,
  exchange TEXT NOT NULL,
  name TEXT,
  sector TEXT,
  currency TEXT DEFAULT 'INR',
  is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS prices (
  symbol TEXT REFERENCES symbols(symbol),
  date DATE NOT NULL,
  open NUMERIC, high NUMERIC, low NUMERIC, close NUMERIC, adj_close NUMERIC,
  volume BIGINT,
  PRIMARY KEY (symbol, date)
);

CREATE TABLE IF NOT EXISTS fundamentals (
  symbol TEXT REFERENCES symbols(symbol),
  period_end DATE NOT NULL,
  period CHAR(1) NOT NULL CHECK (period IN ('Q','Y')),
  pe NUMERIC, pb NUMERIC, ps NUMERIC, ev_ebitda NUMERIC,
  eps NUMERIC, roe NUMERIC, roce NUMERIC, dy NUMERIC, d2e NUMERIC,
  reported_at TIMESTAMP WITH TIME ZONE,  -- public timestamp (for leak-safe lagging)
  PRIMARY KEY (symbol, period_end, period)
);

CREATE TABLE IF NOT EXISTS news (
  id BIGSERIAL PRIMARY KEY,
  symbol TEXT REFERENCES symbols(symbol),
  published_at TIMESTAMPTZ NOT NULL,
  source TEXT,
  title TEXT,
  body TEXT,
  url TEXT
);

CREATE TABLE IF NOT EXISTS nlp_features (
  id BIGSERIAL PRIMARY KEY,
  symbol TEXT REFERENCES symbols(symbol),
  window_end TIMESTAMPTZ NOT NULL,      -- e.g., day boundary
  s_pos DOUBLE PRECISION,
  s_neg DOUBLE PRECISION,
  s_neu DOUBLE PRECISION,
  s_compound DOUBLE PRECISION,
  article_count INT,
  topic_dist JSONB,
  UNIQUE (symbol, window_end)
);

CREATE TABLE IF NOT EXISTS predictions (
  symbol TEXT REFERENCES symbols(symbol),
  asof_date DATE NOT NULL,
  horizon TEXT NOT NULL,                 -- '1d' | '1w'
  p_up DOUBLE PRECISION,
  p_down DOUBLE PRECISION,
  p_neu DOUBLE PRECISION,
  y_hat_close NUMERIC,                   -- regression option
  model_version TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (symbol, asof_date, horizon, model_version)
);

CREATE TABLE IF NOT EXISTS model_runs (
  id BIGSERIAL PRIMARY KEY,
  model_version TEXT,
  started_at TIMESTAMPTZ,
  finished_at TIMESTAMPTZ,
  params JSONB,
  metrics JSONB,
  notes TEXT
);
