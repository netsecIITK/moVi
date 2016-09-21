package main

import (
    "io/ioutil"
    "log"
    "os"
)

var (
    Trace *log.Logger
    Info  *log.Logger
    Warn  *log.Logger
    Error *log.Logger
)

// Called on load of source file
func init() {
    Trace = log.New(ioutil.Discard,
        "[TRACE] ",
        log.Ltime|log.Lshortfile)

    Info = log.New(os.Stdout,
        "[INFO ] ",
        log.Ltime|log.Lshortfile)

    Warn = log.New(os.Stdout,
        "[WARN ] ",
        log.Ltime|log.Lshortfile)

    Error = log.New(os.Stderr,
        "[ERROR] ",
        log.Ltime|log.Lshortfile)
}
