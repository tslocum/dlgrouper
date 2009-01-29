import sys, os, math, random

print """ ____  _        ____                                 
|  _ \| |      / ___|_ __ ___  _   _ _ __   ___ _ __ 
| | | | |     | |  _| '__/ _ \| | | | '_ \ / _ \ '__|
| |_| | |___  | |_| | | | (_) | |_| | |_) |  __/ |   
|____/|_____|  \____|_|  \___/ \__,_| .__/ \___|_|   
                                    |_|           v0.1
       Programmed by Trevor "tj9991" Slocum  
          tj9991.com - tslocum@gmail.com

Instructions:
Type row number to place guests in, then press enter.
To place in two rows, type first row, press space,
then type second row and press enter.
To send the current load press enter.
To exit at any time press Control + C.

Select attraction:"""

attraction_names = ["Indiana Jones Adventure",
                    "Pirates of the Caribbean",
                    "Matterhorn Bobsleds",
                    "Big Thunder Mountain Railroad",
                    "Space Mountain",
                    "It's a Small World"]

i = 0
for attraction_name in attraction_names:
  i += 1
  print " %s) %s" % (str(i), attraction_name),
  if i % 2 == 0:
    print

# Fill attractions variable with data in the format of
# seats per row, rows
attractions = {1: [4, 3],
               2: [4, 5],
               3: [1, 4],
               4: [2, 15],
               5: [2, 6],
               6: [2, 5]}

interrupt = False
while True:
  try:
    attraction_id = int(raw_input(">"))
    if 0 < attraction_id < 7:
      break
  except KeyboardInterrupt:
    interrupt = True
    break
  except:
    pass

def attractionName(attraction_id):
  attraction_id -= 1
  return attraction_names[attraction_id]

def newTrain():
  train = []
  for i in range(attraction[1]):
    row = []
    
    for j in range(attraction[0]):
      row.append(0) # Seat indicating no rider present
      
    train.append(row)
    
  return train

def emptySeatsInRow(train, rownum):
  emptyseats = 0
  for seat in train[rownum]:
    if seat == 0:
      emptyseats += 1

  return emptyseats

def fillSeats(train, rownum, seats):
  seatnum = 0
  for seat in train[rownum]:
    if seat == 0:
      for i in range(seats):
        train[rownum][seatnum] = 1
        seatnum += 1
      break
    seatnum += 1

  return train

def checkSeatIsEmpty(train, rownum, seatnum):
  if train[rownum][seatnum] == 0:
    return True
  else:
    return False

def printStation(attraction_id, attraction, train):
  print attractionName(attraction_id)
  print
  print '-' * ((attraction[1] * 5) + 1)
  for seat in range(0, attraction[0]):
    print '|',
    for row in range(attraction[1]):
      if checkSeatIsEmpty(train, row, seat):
        print 'O', ' |',
      else:
        print 'X  |',
    print
    
  print '-' * ((attraction[1] * 5) + 1)
  print
  print ' ',
  
  for i in range(1, attraction[1] + 1):
    if i < 10:
      print str(i), "  ",
    else:
      print str(i), " ",
      
  print
  print

def checkCouldBeFilled(train, seats):
  rownum = 0
  for row in train:
    if emptySeatsInRow(train, rownum) >= seats:
      return True
    rownum += 1
        
  return False

def trainScore(train):
  score = 0
  for row in train:
    for seat in row:
      if seat != 0:
        score += 1
        
  return score

def newGroup(attraction):
  random_number = random.randint(1, 65)
  if random_number < 10:
    return 1
  elif random_number < 25:
    return random.randint(attraction[0], attraction[0] * 2)
  elif random_number < 40:
    return random.choice([2, 4])
  else:
    return 3

def checkAnyRiderAlone(train, attraction, row1_emptyseats, row2_emptyseats, groupsize):
  if attraction[0] > 1 and ((row1_emptyseats == 1) or ((groupsize - row1_emptyseats) == 1)):
    if (row2_emptyseats == 1) or (((groupsize - row1_emptyseats) + row2_emptyseats) <= 1):  
      return True

    fillSeats(train, row1, (row1_emptyseats - 1))
    fillSeats(train, row2, (groupsize - row1_emptyseats) + 1)
    return False
  
  fillSeats(train, row1, row1_emptyseats)
  fillSeats(train, row2, (groupsize - row1_emptyseats))
  return False

def messup(message):
  global messups, skip_new_group
  print message
  print "Press Enter to continue..."
  messups += 1
  skip_new_group = True
  raw_input()

def clearScreen():
  os.system(['clear','cls'][os.name == 'nt'])

if not interrupt:
  attraction = attractions[attraction_id]
  
  train = newTrain()
  trains_sent = int(0)
  messups = int(0)
  score = int(0)
  row = int(0)
  board_rows = " "
  groupsize = newGroup(attraction)

  while True:
    skip_new_group = False
    clearScreen()
    print "Points: ", str(int(score)), "-", str(trains_sent), "trains sent", "-", messups, "mistakes"
    printStation(attraction_id, attraction, train)

    board_rows = raw_input(str(groupsize) + " to board. Place in row(s): ")

    if len(board_rows) == 0:
      if not checkCouldBeFilled(train, groupsize):
        score += trainScore(train)
        trains_sent += 1
        train = newTrain()
        skip_new_group = True
      else:
        messup("There is enough room for those guests in a single row!")
    elif " " not in board_rows:
      row = int(board_rows) - 1
      if emptySeatsInRow(train, row) >= groupsize:
        fillSeats(train, row, groupsize)
      else:
        messup("There is not enough room in that row for those guests!")
    else:
      split_rows = str(board_rows).split(" ")
      if len(split_rows[1]) == 0:
        print "You only entered one row, but you typed a space!"
        print "This doesn't count as a mistake, but be careful!"
        print "Press Enter to continue..."
        raw_input()
        skip_new_group = True
      else:
        row1 = (int(split_rows[0]) - 1)
        row2 = (int(split_rows[1]) - 1)
        if False: #emptySeatsInRow(train, row1) >= groupsize or emptySeatsInRow(train, row2) >= groupsize: IGNORE THIS
          messup("There is enough room to place that group in one row!")
        else:
          row1_emptyseats = emptySeatsInRow(train, row1)
          row2_emptyseats = emptySeatsInRow(train, row2)
          if row1_emptyseats >= groupsize or (row1_emptyseats < groupsize and row2_emptyseats >= groupsize):
            messup("here is enough room in for those guests in just one row!")
          else:
            if (row1_emptyseats + row2_emptyseats) < groupsize:
              messup("There is not enough room in for those guests in the provided rows!")
            else:
              if checkAnyRiderAlone(train, attraction, row1_emptyseats, row2_emptyseats, groupsize):
                messup("Groups can not be split to any less than two people next to each other!")

    if messups == 4:
      print "Too many mistakes!"
      print "You're FIRED!"
      break
    
    if trains_sent == 25:
      clearScreen()
      print "End of Round"
      print "-----------------------"
      print str(trains_sent), "trains sent"
      print
      if messups > 0:
        print str(messups), "mistakes"
        if score > 0:
          penalty = math.floor(score / (5 - messups))
          print str(int(penalty)), "penalty"
          score -= penalty
        print
      print "Final Score:", str(int(score))
      break

    if not skip_new_group:
      groupsize = newGroup(attraction)
