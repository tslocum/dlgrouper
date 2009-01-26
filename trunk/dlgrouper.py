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
               2: [3, 5],
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
        print 'X', ' |',
    print
    
  print '-' * ((attraction[1] * 5) + 1)
  print
  print ' ',
  
  for i in range(1, attraction[1] + 1):
    if i < 10:
      print str(i), '  ',
    else:
      print str(i), ' ',
      
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

def clearScreen():
  os.system(['clear','cls'][os.name == 'nt'])

if not interrupt:
  attraction = attractions[attraction_id]
  
  train = newTrain()
  trains_sent = 0
  messups = 0
  score = 0

  while True:
    clearScreen()
    print "Points: ", str(score), "-", str(trains_sent), "trains sent", "-", messups, "mistakes"
    printStation(attraction_id, attraction, train)
    groupsize = random.randint(1, 4)
    
    rows = raw_input(str(groupsize) + " to board. Place in row(s): ")
    
    if len(rows) == 0:
      if not checkCouldBeFilled(train, groupsize):
        score += trainScore(train)
        trains_sent += 1
        train = newTrain()
      else:
        print "There is enough room for those guests in a single row!"
        print "Press Enter for next group..."
        messups += 1
        raw_input()
    elif len(rows) == 1:
      row = (int(rows) - 1)
      if emptySeatsInRow(train, row) >= groupsize:
        fillSeats(train, row, groupsize)
      else:
        print "There is not enough room in that row for those guests!"
        print "Press Enter for next group..."
        messups += 1
        raw_input()
    elif len(rows) > 1:
      rows = str(rows).split(' ')
      row1 = (int(rows[0]) - 1)
      row2 = (int(rows[1]) - 1)
      if emptySeatsInRow(train, row1) >= groupsize or emptySeatsInRow(train, row2) >= groupsize:
        print "There is enough room to place that group in one row!"
        print "Press Enter for next group..."
        messups += 1
        raw_input()
      else:
        row1_emptyseats = emptySeatsInRow(train, row1)
        row2_emptyseats = emptySeatsInRow(train, row2)
        if row1_emptyseats < groupsize and row2_emptyseats < (groupsize - row1_emptyseats):
          print "There is not enough room in for those guests in the provided rows!"
          print "Press Enter for next group..."
          messups += 1
          raw_input()
        else:
          fillSeats(train, row1, row1_emptyseats)
          fillSeats(train, row2, (groupsize - row1_emptyseats))

    if messups == 4:
      print "Too many mistakes!"
      print "You're FIRED!"
      break
    
    if trains_sent == 10:
      clearScreen()
      print "End of Round"
      print "-----------------------"
      print str(trains_sent), "trains sent"
      print
      if messups > 0:
        print str(messups), "mistakes"
        if score > 0:
          penalty = math.floor(score / (5 - messups))
          print str(penalty) + "penalty"
          score -= penalty
        print
      print "Final Score:", str(score)
      break
