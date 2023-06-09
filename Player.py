import numpy as np

from OtrioArtist import * # colors, pieces, artist class

# A Player has 27 places he can put pieces, 9 SMA, 9 MED and 9 BIG
# and the player will hold a list of 27 flags for which of those have pieces.
# There are 49 unique winning configurations (per player, total 196).
# This function will generate and return the whole list so they can
# generate them once, at construction, and hold the list for convenient
# looping through to check for winning moves

def all_winning_triples():
    win_trip = []

    #3-Ring wins (e.g. SMB at position (0,0,0))
    for i in range(9):
        snum = i
        mnum = i + 9
        bnum = i + 18
        win_trip.append((snum, mnum, bnum))

    #Same-Size / Diff-Size Wins
    win_trip2 = [(0,1,2), (3,4,5), (6,7,8),              #SMA-h
                 (9,10,11), (12,13,14), (15,16,17),      #MED-h
                 (18,19,20), (21,22,23), (24,25,26),     #BIG-h
                 (0,3,6), (1,4,7), (2,5,8),              #SMA-v
                 (9,12,15), (10,13,16), (11,14,17),      #MED-v
                 (18,21,24), (19,22,25), (20,23,26),     #BIG-v
                 (0,4,8), (2,4,6),                       #SMA-d
                 (9,13,17), (11,13,15),                  #MED-d
                 (18,22,26), (20,22,24),                 #BIG-d
                 (0,10,20), (3,13,23), (6,16,26),        #SMB-h
                 (0,12,24), (1,13,25), (2,14,26),        #SMB-v
                 (0,13,26), (2,13,24),                   #SMB-d
                 (18,10,2), (21,13,5), (24,16,8),        #BMS-h
                 (18,12,6), (19,13,7), (20,14,8),        #BMS-v
                 (18,13,8), (20,13,6)]                   #BMS-d
    win_trip.extend(win_trip2)
    return win_trip

class Player:
    def __init__(self, c, bc):
        '''
        A Player knows what color his pieces are, and
        holds an array of 27 flags for whether pieces are placed
        :param c: What color is this player's pieces?
        '''
        self.color = c                         # what color am I
        self.bright = bc                       # all_wins highlighted by bright color
        self.flags = [False]*27                # No pieces played to start
        self.wintrips = all_winning_triples()  # know where the wins are

    def convert_to_wh(self, index):
        '''
        Convert overall index of position to WHICH piece and WHERE to put it
        :param index:
        :return:  which where to index calculation
        '''
        return (index//9+1, index%9)

    def convert_to_ind(self, which, where):
        '''
        Convert WHICH piece and WHERE to put it into overall index of position
        :param which:
        :param where:
        :return: index to which/where calculation
        '''
        return (which - 1) * 9 + where

    def place(self, which=None, where=None, index=None):
        '''
        Set the appropriate flag to indicate a played piece
        :param which: SMA, MED, or BIG
        :param where: Position index 0-8
        :param index: Flag index 0-26
        :return: None
        '''
        if index is None:
            index = self.convert_to_ind(which,where)
        self.flags[index] = True

    def remove(self, which=None, where=None, index=None):
        '''
        Set the appropriate flag to indicate a removed piece
        :param which: SMA, MED, or BIG
        :param where: Position index 0-8
        :param index: Flag index 0-26
        :return: None
        '''
        if index is None:
            index = self.convert_to_ind(which, where)
        self.flags[index] = False

    def num_played(self, which):
        '''
        Track the number of pieces played
        :param which:
        :return: sum of segment of indices for each size
        '''
        if which == SMA:
            return sum(self.flags[0:9])
        elif which == MED:
            return sum(self.flags[9:18])
        elif which == BIG:
            return sum(self.flags[18:27])

    def num_remaining(self, which):
        '''
        Track the number of pieces of each size remaining
        :param which:
        :return: number of remaining pieces of each size
        '''
        return (3 - self.num_played(which))

    def remaining_pieces(self):
        '''
        Track pieces remaining in hand after placing a piece on the board
        :return: Updated list of pieces
        '''
        #sum_array = np.array(self.flags)
        smalls_remaining = self.num_remaining(SMA)
        meds_remaining = self.num_remaining(MED)
        bigs_remaining = self.num_remaining(BIG)
        return (smalls_remaining, meds_remaining, bigs_remaining)

    def draw(self, board):
        '''
        Draw all this player's active pieces onto an OtrioArtist
        :param board: an OtrioArtist (may have other Player's pieces already drawn)
        :return: None
        '''
        for index in range(len(self.flags)):
            if self.flags[index]:
                which, where = self.convert_to_wh(index)
                board.draw_piece(which, self.color, where)
            if self.all_wins():
                for trip in self.all_wins():
                    for index in trip:
                        which, where = self.convert_to_wh(index)
                        board.draw_piece(which, self.bright, where)


    def has_all_pieces(self, indices):
        '''
        Go through a list of indices (probably one of the winning 3-tuples)
        and check if all of the flags at those indices are True (pieces are placed there)
        :param indices:
        :return: True if all the indices are played, False if any are not
        '''
        for i in indices:
            if self.flags[i] == False:
                return False
        return True

    def has_a_win(self):
        '''
        Check through the possible winning index triplets, if a win is found, return
        that tuple and stop searching. Otherwise return False
        :return: the 3-tuple of winning indices, or False
        '''
        for trip in self.wintrips:
            if self.has_all_pieces(trip):
                return trip
        return False

    def all_wins(self):
        '''
        Return a list of all winning triplets that are present in this Player's
        pieces, not just the first one found
        :return: list of winning 3-tuples (empty list if not a winning position)
        '''
        wins = []
        for trip in self.wintrips:
            if self.has_all_pieces(trip):
                wins.append(trip)
        return wins



if __name__ == '__main__':
    p = Player(RED, REDl)


    #Generate images to check all winning triplets
    if False:
        for i, trip in enumerate(p.wintrips):
            for index in trip:
                p.place(index=index)
            board = OtrioArtist()
            p.draw(board)
            board.im_save('win_trip_{}.png'.format(i))
            for index in trip:
                p.remove(index=index)



    p.place(SMA, 4)
    p.place(SMA, 8)
    #should_be_True = p.piece_size_remaining(SMA)
    p.place(SMA, 6)
    numplay_test = p.num_played(SMA)
    #should_be_False = p.piece_size_remaining(SMA)
    rem_pieces = p.remaining_pieces()
    #test = np.array(p.flags)
    #test_s = test[0:9]
    #nptest = test_s.sum()
    full1 = p.has_all_pieces([4])
    full2 = p.has_all_pieces([4,8])
    full3 = p.has_all_pieces([2])
    full4 = p.has_all_pieces([4+9,8+9])
    should_be_false = p.has_a_win()
    p.place(SMA, 2)
    p.place(SMA, 0)
    p.place(SMA, 1)
    p.place(BIG, 0)
    p.place(BIG, 1)
    p.place(BIG, 2)
    p.place(index=24)
    p.place(index=12)
    #should_be_False2 = p.piece_size_remaining(BIG)
    winner = p.has_a_win()
    winners = p.all_wins()
    should_be_one = len(winners)
    p.place(SMA, 1)
    winner = p.has_a_win()
    winners = p.all_wins()
    should_be_two = len(winners)

    board = OtrioArtist()
    p.draw(board)
    board.im_save('gs_test1.png')
