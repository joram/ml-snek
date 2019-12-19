package main

import (
	"github.com/davecgh/go-spew/spew"
	"github.com/joram/ml-snek/api"
	deep "github.com/patrikeh/go-deep"
	"github.com/patrikeh/go-deep/training"
	"image/jpeg"
	"math"
	"os"
	"fmt"
	"path/filepath"
	"strings"
)

func main(){
	fmt.Println("loading training data...")
	var data = getTrainingData("../../images", -1)
	spew.Dump(data[len(data)-1])

	fmt.Println("building neural net...")
	numInputs := len(data[0].Input)
	fmt.Println(numInputs)
	n := deep.NewNeural(&deep.Config{
		/* Input dimensionality */
		Inputs: numInputs,
		/* Two hidden layers consisting of two neurons each, and a single output */
		Layout: []int{numInputs, 20, 1},
		/* Activation functions: Sigmoid, Tanh, ReLU, Linear */
		//Activation: deep.ActivationSigmoid,

		// cause wild changes
		Activation: deep.ActivationLinear,
		Mode: deep.ModeDefault,

		//Activation: deep.ActivationLinear,
		//Mode: deep.ModeRegression,
		/* Determines output layer activation & loss function:
		ModeRegression: linear outputs with MSE loss
		ModeMultiClass: softmax output with Cross Entropy loss
		ModeMultiLabel: sigmoid output with Cross Entropy loss
		ModeBinary: sigmoid output with binary CE loss */
		/* Weight initializers: {deep.NewNormal(μ, σ), deep.NewUniform(μ, σ)} */
		Weight: deep.NewNormal(1.0, 0.0),
		/* Apply bias */
		Bias: true,
	})
	fmt.Println("training neural net...")
	optimizer := training.NewAdam(0.05, 0.9, 0.999, 1e-8)
	// params: learning rate, momentum, alpha decay, nesterov
	//optimizer := training.NewSGD(0.05, 0.1, 1e-6, true)
	//trainer := training.NewBatchTrainer(optimizer, 1, 200, 8)
	trainer := training.NewTrainer(optimizer, 50)
	training2, heldout := data.Split(0.5)
	trainer.Train(n, training2, heldout, 1000)

	fmt.Println("checking neural net...")
	valid := 0
	invalid := 0
	for _, d := range data {
		left := n.Predict(d.Input)[0]
		right := n.Predict(d.Input)[1]
		up := n.Predict(d.Input)[2]
		down := n.Predict(d.Input)[3]
		closest := math.Max(math.Max(math.Max(left, right), up), down)

		direction := api.UNKNOWN
		if closest == left { direction = api.LEFT }
		if closest == right { direction = api.RIGHT }
		if closest == up { direction = api.UP }
		if closest == down { direction = api.DOWN }
		if direction == int(d.Response[0]) {
			valid += 1
		} else {
			invalid += 1
		}
	}
	fmt.Printf("%s valid,\t %s invalid\n", valid, invalid)
}

func getTrainingData(path string, maxSize int) training.Examples {
	data := training.Examples{}
	//i := 0
	err := filepath.Walk(path, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			panic(err)
		}
		//i += 1
		//if i >= maxSize && maxSize != -1 {
		//	return nil
		//}
		parts := strings.Split(strings.Replace(path, ".jpg", "", 1), "::")
		if len(parts) == 2 {
			direction := parts[1]
			file, err := os.Open(path)
			defer file.Close()
			if err != nil {
				panic(err)
			}

			img, err := jpeg.Decode(file)
			if err != nil {
				panic(err)
			}

			var input []float64
			for y := 0; y < img.Bounds().Max.Y; y++ {
				for x := 0; x < img.Bounds().Max.X; x++ {
					// color := img.At(x, y)
					r,g,b,_ := img.At(x, y).RGBA()
					input = append(input, float64(r%256))
					input = append(input, float64(g%256))
					input = append(input, float64(b%256))
				}
			}

			//var response []float64
			//left := []float64{255,0,0,0}
			//right := []float64{0,255,0,0}
			//up := []float64{0,0,255,0}
			//down := []float64{0,0,0,255}
			//if api.StringToDir(direction) == api.LEFT {response = left}
			//if api.StringToDir(direction) == api.RIGHT {response = right}
			//if api.StringToDir(direction) == api.UP {response = up}
			//if api.StringToDir(direction) == api.DOWN {response = down}

			response := []float64{float64(api.StringToDir(direction))*256/4}

			data = append(data, training.Example{
				Input: input,
				Response: response,
			})
		} else {
			fmt.Println(path)
		}
		return nil
	})
	if err != nil {
		panic(err)
	}
	return data
}
