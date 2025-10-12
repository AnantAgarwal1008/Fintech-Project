package main

import (
	"log"
	"os"

	"github.com/gin-gonic/gin"

	"AnantAgarwal1008/internal"
)

func main() {
	db, err := internal.NewDB()
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	r := gin.Default()
	r.GET("/health", internal.Health())
	r.GET("/predictions", internal.GetPredictions(db))

	port := os.Getenv("API_PORT")
	if port == "" { port = "8080" }
	log.Printf("API listening on :%s", port)
	_ = r.Run(":" + port)
}
