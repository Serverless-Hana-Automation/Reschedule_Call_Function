from src import app
import os

def main():

  input_file = os.path.join("")
  num_of_sheets = 9
  app.split_numbers(input_file, num_of_sheets)


  initialTimestamp = "2030-08-31T09:00:00+08:00"
  split_batches = app.split_numbers(input_file, num_of_sheets)
  app.hourUpload(initialTimestamp,split_batches)
  

if __name__ == "__main__":
  main()



