package main

import (
    "io/ioutil"
    "os"
)

func main() {
    LogInit(ioutil.Discard, os.Stdout, os.Stdout, os.Stderr)

    Trace.Println("Non printing")
    Info.Println("Info")
    Warn.Println("Warn")
    Error.Println("Failed")
}
