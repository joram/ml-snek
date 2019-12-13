package main

import (
	"fmt"
	"encoding/json"
	"github.com/davecgh/go-spew/spew"
	"github.com/joram/ml-snek/util"
	"github.com/joram/ml-snek/api"
)

func isDead(snake api.Snake, sr api.SnakeRequest) bool {
	head := snake.Head()
	if head.X < 0 || head.X > sr.Board.Width-1 {
		return true
	}
	if head.Y < 0 || head.Y > sr.Board.Height-1 {
		return true
	}
	for _, otherSnake := range sr.Board.Snakes {
		if otherSnake.ID == snake.ID {
			continue
		}
		isBigger := len(otherSnake.Body) > len(snake.Body)
		for _, coord := range otherSnake.Body {
			if head.Equal(coord) && isBigger {
				return true
			}
		}
	}
	return false
}

func main(){
	for _, key := range util.ListS3("jsnek") {

		var snakeRequests []api.SnakeRequest
		content := util.GetFromS3("jsnek", key)
		err := json.Unmarshal(content, &snakeRequests)
		if err != nil {
			spew.Dump(err)
			continue
		}

		lastSnakeRequest := snakeRequests[len(snakeRequests)-1]
		if len(lastSnakeRequest.OtherSnakes()) != 1 {
			continue
		}
		winner := lastSnakeRequest.OtherSnakes()[0]
		fmt.Printf("https://play.battlesnake.com/g/%s/ \t%s\n", lastSnakeRequest.Game.ID, winner.Name)
		bitmaps(snakeRequests, winner.ID)
	}
}

func bitmaps(snakeRequests []api.SnakeRequest, snakeID string) {
	for _, sr := range snakeRequests {
		bitmap(sr, snakeID)
	}
}

const size = 9
func bitmap(sr api.SnakeRequest, snakeID string) [size][size]int {
	head := api.Coord{}
	for _, snake := range sr.Board.Snakes {
		if snake.ID == snakeID {
			head = snake.Head()
			break
		}
	}

	heatmap := [size][size]int{}
	for _, snake := range sr.Board.Snakes {
		prev := api.Coord{}
		for i, coord := range snake.Body {
			if coord == prev {
				continue
			}
			prev = coord

			offset := (size-1)/2
			offsetCoord := coord.Offset(- head.X + offset, - head.Y + offset)
			if offsetCoord.X < 0 || offsetCoord.X >= size {
				continue
			}
			if offsetCoord.Y < 0 || offsetCoord.Y >= size {
				continue
			}

			heatmap[offsetCoord.X][offsetCoord.Y] = len(snake.Body) - i
		}
	}
	for _, r := range heatmap {
		fmt.Println(r)
	}
	fmt.Println("")

	return heatmap
}