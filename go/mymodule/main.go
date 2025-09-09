package main

import (
	"fmt"
	"mymodule/mypackage"
	"github.com/spf13/cobra"
)

func main() {
	
	cmd := &cobra.Command{
		Run: func(cmd *cobra.Command, args []string) {

	fmt.Println("Hello, Modules!")
	mypackage.PrintHello()
	},

}

fmt.Println("Calling cmd.Execute()!")
cmd.Execute()

}
