package main

import (
	"encoding/json"
	"fmt"
	"github.com/davecgh/go-spew/spew"
	"github.com/joram/ml-snek/api"
	"github.com/joram/ml-snek/util"
	"image"
	"image/color"
	"image/jpeg"
	"os"
)

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
	for i, sr := range snakeRequests {
		var next *api.SnakeRequest
		if i < len(snakeRequests)-1 {
			next = &snakeRequests[i+1]
			createImage(&sr, next, snakeID)
		}
	}
}

func createImage(sr, next *api.SnakeRequest, snakeID string){
	img := image.NewRGBA(image.Rect(0, 0, sr.Board.Width, sr.Board.Height))

	// age of body
	for _, snake := range sr.Board.Snakes {
		for i := 0; i < len(snake.Body); i++ {
			x := len(snake.Body) - i
			c := color.RGBA{uint8(x),0,0,255}
			coord := snake.Body[i]
			img.Set(coord.X, coord.Y, c)
		}
	}

	// food
	for _, food := range sr.Board.Food {
		c := color.RGBA{0,255,0,255}
		img.Set(food.X, food.Y, c)
	}

	// my head
	head := sr.GetSnake(snakeID).Head()
	c := color.RGBA{0,0,255,255}
	img.Set(head.X, head.Y, c)

	// figure out direction
	var currHead api.Coord
	for _, snake := range sr.Board.Snakes {
		if snake.ID == snakeID {
			currHead = snake.Head()
			break
		}
	}
	var nextHead api.Coord
	for _, snake := range next.Board.Snakes {
		if snake.ID == snakeID {
			nextHead = snake.Head()
			break
		}
	}
	d := currHead.NearestDirectionTo(nextHead)
	direction := api.DirToString(d)

	// Save output to png
	filename := fmt.Sprintf("../../images/%s_%d::%s.jpg", sr.Game.ID, sr.Turn, direction)
	f, _ := os.OpenFile(filename, os.O_WRONLY|os.O_CREATE, 0600)
	defer f.Close()
	jpeg.Encode(f, img, nil)

}