package model

var Opts Options

type IOOptions struct {
	InputFile    string `short:"i" long:"input-file" description:"The input file" required:"true" default:"input.txt"`
	OutputFolder string `short:"o" long:"output-folder" description:"The output folder" required:"true" default:"output"`
}

type Options struct {
	IOOptions
	Timeout                int  `short:"t" long:"timeout" description:"Timeout of each HTTP request (in seconds)" default:"16"`
	NumWorkers             int  `short:"n" long:"num-workers" description:"Number of workers" default:"8"`
	NumGoroutinesPerWorker int  `short:"g" long:"num-goroutines-per-worker" description:"Number of goroutines per worker" default:"16"`
	Debug                  bool `short:"d" long:"debug" description:"Enable debug mode"`
	Version                bool `short:"v" long:"version" description:"Version"`
}
