package main

import (
    "io"
    "log"
)

var (
    Trace *log.Logger
    Info  *log.Logger
    Warn  *log.Logger
    Error *log.Logger
)

func LogInit(
    traceHandle io.Writer,
    infoHandle io.Writer,
    warningHandle io.Writer,
    errorHandle io.Writer) {

    Trace = log.New(traceHandle,
        "[TRACE] ",
        log.Ltime|log.Lshortfile)

    Info = log.New(infoHandle,
        "[INFO ] ",
        log.Ltime|log.Lshortfile)

    Warn = log.New(warningHandle,
        "[WARN ] ",
        log.Ltime|log.Lshortfile)

    Error = log.New(errorHandle,
        "[ERROR] ",
        log.Ltime|log.Lshortfile)
}
