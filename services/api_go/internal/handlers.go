package internal

import (
	"context"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

func Health() gin.HandlerFunc {
	return func(c *gin.Context) { c.JSON(http.StatusOK, gin.H{"ok": true}) }
}

func ListSymbols(db pgx.Tx) ([]string, error) { return nil, nil }

func GetPredictionsHandler(dbpool pgx.Tx) gin.HandlerFunc { return nil }

// Simple, readable version:
func GetPredictions(db *pgxpool.Pool) gin.HandlerFunc {
	return func(c *gin.Context) {
		symbol := c.Query("symbol")
		horizon := c.DefaultQuery("horizon", "1d")
		asof := c.Query("asof") // optional YYYY-MM-DD

		q := `
		select symbol, asof_date, horizon, p_up, p_down, p_neu, model_version
		from predictions
		where symbol=$1 and horizon=$2
		`
		args := []any{symbol, horizon}
		if asof != "" {
			q += " and asof_date=$3"
			args = append(args, asof)
		} else {
			q += " order by asof_date desc limit 1"
		}

		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()

		rows, err := db.Query(ctx, q, args...)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		defer rows.Close()

		type rowT struct {
			Symbol, AsofDate, Horizon, ModelVersion string
			PUp, PDown, PNeu                        float64
		}
		var out []rowT
		for rows.Next() {
			var r rowT
			if err := rows.Scan(&r.Symbol, &r.AsofDate, &r.Horizon, &r.PUp, &r.PDown, &r.PNeu, &r.ModelVersion); err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
				return
			}
			out = append(out, r)
		}
		c.JSON(http.StatusOK, out)
	}
}
