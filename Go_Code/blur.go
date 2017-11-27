package main

import (
    "image"
    "image/png"
    "os"
    "fmt"
    "math"
)

func main() {
    infile, err := os.Open(os.Args[1])
    if err != nil {
        fmt.Println("Error: Open")
    }
    defer infile.Close()

    src, _, err := image.Decode(infile)
    if err != nil {
        fmt.Println("Error: Decode")
    }
    var sig float64 = 3
    var param float64 = 1.92
    var fac float64 = 1/(math.Pi * 2 * sig * sig)
    var weight float64

    bounds := src.Bounds()
    W, H := bounds.Max.X, bounds.Max.Y
    gray := image.NewRGBA(bounds)
    for w := int(sig); w < W-int(sig); w++ {
        for h := int(sig); h < H-int(sig); h++ {
            oldColor := src.At(w, h)
            gray.Set(w, h, oldColor)
            var red float64   = 0
            var blue float64  = 0
            var green float64 = 0

            var exp_input float64
            var weight_sum float64 = 0

            for ww := w-int(sig); ww < w+1+int(sig); ww++ {
                for hh := h-int(sig); hh < h+1+int(sig); hh++ {

                    var wf float64 = float64(w)
                    var hf float64 = float64(h)
                    var wwf float64 = float64(ww)
                    var hhf float64 = float64(hh)

                    exp_input = -((wf-wwf)*(wf-wwf) + (hf-hhf)*(hf-hhf))
                    exp_input /= (2*sig*sig)
                    weight = fac * math.Exp(exp_input)
                    red += weight * float64(gray.Pix[(hh * W + ww) * 4])
                    blue += weight * float64(gray.Pix[(hh * W + ww) * 4 + 1])
                    green += weight * float64(gray.Pix[(hh * W + ww) * 4 + 2])
                    weight_sum += weight
                }
            }

            gray.Pix[(h * W + w) * 4 ] = uint8(red / weight_sum * param)
            gray.Pix[(h * W + w) * 4 + 1] = uint8(blue / weight_sum * param)
            gray.Pix[(h * W + w) * 4 + 2] = uint8(green / weight_sum * param)
        }
    }
    outfile, err := os.Create(os.Args[2])
    if err != nil {
        fmt.Println("Error Create")
    }
    defer outfile.Close()
    png.Encode(outfile, gray)
}
