package api

func (sr SnakeRequest) MyEmptyAdjacents() []Coord {
	var choices []Coord
	for _, a := range sr.You.Head().Adjacent() {
		if sr.Board.IsEmpty(a) {
			choices = append(choices, a)
		}
	}
	return choices
}

func (sr SnakeRequest) OtherSnakes() []Snake {
	var otherSnakes []Snake
	for _, s := range sr.Board.Snakes {
		if s.ID != sr.You.ID {
			otherSnakes = append(otherSnakes, s)
		}
	}
	return otherSnakes
}


func (sr SnakeRequest) GetSnake(id string) *Snake {
	for _, snake := range sr.Board.Snakes {
		if snake.ID == id {
			return &snake
		}
	}
	return nil
}