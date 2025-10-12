CREATE INDEX IF NOT EXISTS idx_prices_symbol_date ON prices(symbol, date);
CREATE INDEX IF NOT EXISTS idx_news_symbol_time ON news(symbol, published_at);
CREATE INDEX IF NOT EXISTS idx_nlp_symbol_time ON nlp_features(symbol, window_end);
CREATE INDEX IF NOT EXISTS idx_preds_symbol_date ON predictions(symbol, asof_date);
