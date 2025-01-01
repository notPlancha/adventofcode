open System.IO
open FSharp.Data

let here (path: string) = Path.Combine(__SOURCE_DIRECTORY__, path)
let reports = here("input.txt") |>
              File.ReadAllLines |>
              Array.map(
                fun line -> line.Split(" ") |> fun arr -> [for i in arr -> int(i)] |> Array.ofList) 

// let csv: CsvFile = here("input.txt") |> CsvFile.Load(" ")

// print reports that the array is less or equal of 2 len
printf "%A" (reports |> Array.filter(fun arr -> arr.Length <= 2) |> Array.length) // 0

let mutable out = 0
for report in reports do
  let mutable prevLevel = report[0]
  let mutable add_to_out = true
  let decreasing = report[0] > report[1]
  for level in report[1..] do
    if level < prevLevel then
      add_to_out <- false
      break // theres no break in f#, dam this sucks for scripting unless you commit to it