package main

import (
	"context"
	"fmt"
	"log"

	"github.com/SUDEEPBOTS/Waifus-API/clients/go"
)

func main() {
	fmt.Println("🌸 Initializing Go Waifu Client...")
	client := waifus.NewClient("")

	ctx := context.Background()

	// 1. Stats
	stats, err := client.Stats(ctx)
	if err != nil {
		log.Fatalf("Stats error: %v", err)
	}
	fmt.Printf("📊 Total Waifus in Database: %d (%s)\n", stats.TotalRecords, stats.Database)

	// 2. Random Waifu
	fmt.Println("\n🎲 Rolling Random Waifu...")
	w, err := client.Random(ctx)
	if err != nil {
		log.Fatalf("Random error: %v", err)
	}
	fmt.Printf("   Character: %s\n   Rarity:    %s\n   Image:     %s\n", w.Name, w.Rarity, w.ImgURL)
}
