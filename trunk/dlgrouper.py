import sys, os, math, random, re

print """ ____  _        ____                                 
|  _ \| |      / ___|_ __ ___  _   _ _ __   ___ _ __ 
| | | | |     | |  _| '__/ _ \| | | | '_ \ / _ \ '__|
| |_| | |___  | |_| | | | (_) | |_| | |_) |  __/ |   
|____/|_____|  \____|_|  \___/ \__,_| .__/ \___|_|   
                                    |_|           v0.2
       Programmed by Trevor "tj9991" Slocum  
          tj9991.com - tslocum@gmail.com

Instructions:
Type row number to place guests in, then press enter.
To place in two rows, type first row, press space,
then type second row and press enter.
To call out for a group of a certain size, press 
space, then enter the group size desired.
To dispatch the current load press enter.
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

_DEBUG = False
rounds = 15

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
  if attraction[0] == 1:
    return random.randint(1, 2)
    
  random_number = random.randint(1, 65)
  if random_number < 10:
    return 1
  elif random_number < 25:
    return random.randint(attraction[0], attraction[0] * 2)
  elif random_number < 40:
    return random.choice([2, 4])
  else:
    return 3

def newQueue(attraction):
  queue = []
  for i in range(10):
    queue.append(newGroup(attraction))
  return queue

def groupInQueue(currentgroup, wantedgroup):
  global queue, attraction
  if wantedgroup in queue:
    del queue[queue.index(wantedgroup)]
    queue.append(currentgroup)
    return True
  else:
    return False

def nextGroup():
  global queue, attraction
  queue.insert(0, newGroup(attraction))
  return queue.pop()

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

def validRow(attraction, row):
  return (1 <= row <= attraction[1])

def messup(message):
  global messups, skip_new_group
  print message
  print "Press Enter to continue..."
  messups += 1
  skip_new_group = True
  raw_input()

def printSpecial(message):
  sys.stdout.write(message) 
  sys.stout.flush()

def clearScreen():
  os.system(['clear','cls'][os.name == 'nt'])

def isInt(n):
  return re.match("^[-+]?[0-9]+$", n)

if not interrupt:
  attraction = attractions[attraction_id]
  
  train = newTrain()
  trains_sent = int(0)
  messups = int(0)
  score = int(0)
  row = int(0)
  board_rows = " "
  specialmessage = ""
  queue = newQueue(attraction)
  groupsize = nextGroup()

  while True:
    skip_new_group = False
    clearScreen()
    print "Points: ", str(int(score)), "-", str(trains_sent), "trains sent", "-", messups, "mistakes"
    printStation(attraction_id, attraction, train)

    if _DEBUG:
      print "Queue: " + repr(queue) + " <-- Next group"

    if specialmessage != "":
      print specialmessage
    else:
      print
    board_rows = raw_input(str(groupsize) + " to board. Place in row(s): ")
    
    specialmessage = ""

    if len(board_rows) == 0:
      if not checkCouldBeFilled(train, groupsize):
        score += trainScore(train)
        trains_sent += 1
        train = newTrain()
        skip_new_group = True
      else:
        messup("There is enough room for those guests in a single row!")
    elif board_rows[0] == " ":
      mistake = False
      for i in range(0, attraction[1]):
        if emptySeatsInRow(train, i) >= groupsize:
          mistake = True
      if mistake:
        messup("There is enough room in for the current group in just one row!")
      else:
        if isInt(board_rows[1:]):
          wantedgroup = int(board_rows[1:])
          if groupInQueue(groupsize, wantedgroup):
            groupsize = wantedgroup
            specialmessage = "Success!  A group of " + str(wantedgroup) + " now waiting to board."
          else:
            specialmessage = "No groups responded after calling out that group size."
        else:
          print "The format for calling out new groups is a space followed by a group size."
          print "For example, to call out a group of three, type \" 3\""
          print "Press Enter to continue..."
          raw_input()
        skip_new_group = True
    elif " " not in board_rows:
      if isInt(board_rows):
        if validRow(attraction, int(board_rows)):
          row = int(board_rows) - 1
          if emptySeatsInRow(train, row) >= groupsize:
            fillSeats(train, row, groupsize)
          else:
            messup("There is not enough room in that row for those guests!")
        else:
          messup("This attraction doesn't have a row of that number!")
      else:
        print "Whoops!  Only spaces and numbers are allowed!"
        print "This doesn't count as a mistake, but be careful!"
        print "Press Enter to continue..."
        raw_input()
        skip_new_group = True
    else:
      split_rows = str(board_rows).split(" ")
      if len(split_rows[1]) == 0:
        print "You only entered one row, but you typed a space!"
        print "This doesn't count as a mistake, but be careful!"
        print "Press Enter to continue..."
        raw_input()
        skip_new_group = True
      else:
        if isInt(split_rows[0]) and isInt(split_rows[1]):
          if validRow(attraction, int(split_rows[0])) and validRow(attraction, int(split_rows[1])):
            row1 = (int(split_rows[0]) - 1)
            row2 = (int(split_rows[1]) - 1)
            if False: #emptySeatsInRow(train, row1) >= groupsize or emptySeatsInRow(train, row2) >= groupsize: IGNORE THIS
              messup("There is enough room to place that group in one row!")
            else:
              row1_emptyseats = emptySeatsInRow(train, row1)
              row2_emptyseats = emptySeatsInRow(train, row2)
              if row1_emptyseats >= groupsize or (row1_emptyseats < groupsize and row2_emptyseats >= groupsize):
                messup("There is enough room in for those guests in just one row!")
              else:
                if (row1_emptyseats + row2_emptyseats) < groupsize:
                  messup("There is not enough room in for those guests in the provided rows!")
                else:
                  if checkAnyRiderAlone(train, attraction, row1_emptyseats, row2_emptyseats, groupsize):
                    messup("Groups can not be split to any less than two people next to each other!")
          else:
            messup("This attraction doesn't have a row of that number!")
        else:
          print "Whoops!  Only spaces and numbers are allowed!"
          print "This doesn't count as a mistake, but be careful!"
          print "Press Enter to continue..."
          raw_input()
          skip_new_group = True
         
    if messups == 4:
      print "You were reported to your lead, and he has some bad news!"
      print "You're FIRED!"
      print "Press Enter to continue..."
      raw_input()
      break
    
    if trains_sent == rounds:
      clearScreen()
      print "End of Round"
      print "-----------------------"
      print str(trains_sent), "trains sent"
      print str(int(score)), "points"
      print
      if messups > 0:
        print str(messups), "mistakes"
        if score > 0:
          penalty = math.floor(score / (5 - messups))
          print str(int(penalty)), "penalty"
          score -= penalty
        print
      print "Final Score:", str(int(score))
      print "Press Enter to continue..."
      raw_input()
      break

    if not skip_new_group:
      groupsize = groupsize = nextGroup()
