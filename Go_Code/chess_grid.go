package main

import "fmt"
import "image"
import "image/png"
import "image/color"
import "os"

func main () {
    var w, h int = 100, 120

    rect := image.Rect(0, 0, w, h)
    img := image.NewGray(rect)

    for x:= 0; x < w; x+=2 {
        for y:= 0; y < h; y+=2 {
            img.Set(x, y, color.White)
        }
    }

    outfile, err := os.Create(os.Args[1])
    if err != nil {
        fmt.Println(err)
    }
    defer outfile.Close()
    png.Encode(outfile, img)
}
