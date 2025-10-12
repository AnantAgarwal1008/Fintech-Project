package internal

type Prediction struct {
	Symbol      string  `json:"symbol"`
	AsofDate    string  `json:"asof_date"`
	Horizon     string  `json:"horizon"`
	PUp         float64 `json:"p_up"`
	PDown       float64 `json:"p_down"`
	PNeu        float64 `json:"p_neu"`
	YHatClose   *string `json:"y_hat_close,omitempty"`
	ModelVersion string `json:"model_version"`
}
