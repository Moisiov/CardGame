# TIE-02100 Introduction to Programming
# Scaling GUI (Card game)
# Valto Moisio, valto.moisio@student.tut.fi, opiskelijanumero: 268644
# Korttipeli käyttäen tkinteriä
# Status: READY

'''
This is a card game created by Valto Moisio. The game was made as a school
project for the course TIE-02100 Introduction to Programming at Tampere
University of Technology. Difficulty level of this game is: scaling.

Game board contains card decks (buttons) which form a x*x square. Size of the
square, number of players and goal score can be adjusted in first few rows of
the code.

In the left side of the game window you see text labels which tells the active
player, goal score and players scores. In the right there is "New game",
"Guide" and "Quit game" buttons. Rules of the game can be found in "Guide".

First 20 rows of code are necessary imports and a few global variables which
can be adjusted. You can change pictures and window icon by replacing old
pictures in the folder. NOTE: make sure your new pictures are in right format
and named right if you change them.

The class Cardgame __init__ method creates the main window of the game and sets
variables ready.

After __init__, next 7 methods do the calculations and make the game run.

Last methods in class Card game are text updates, functions for "New game",
"Guide" and "Quit game" buttons and the last but not least is method which
calls mainloop.
'''

from tkinter import *
import random
import time

#Can be adjusted
PLAYER_NUMBER = 2
ROWS_AND_COLUMNS = 3 #Needs to be 2 or more
GOAL_SCORE = 25

#DO NOT touch any of these picture names
deck_cover = "0.gif"

card_deck = ["1.gif","2.gif","3.gif","4.gif","5.gif","6.gif","7.gif","8.gif","9.gif",
             "10.gif","11.gif","12.gif","13.gif","14.gif","15.gif","16.gif","17.gif",
             "18.gif","19.gif","20.gif","21.gif","22.gif","23.gif","24.gif","25.gif",
             "26.gif","27.gif","28.gif","29.gif","30.gif","31.gif","32.gif","33.gif",
             "34.gif","35.gif","36.gif","37.gif","38.gif","39.gif","40.gif","41.gif",
             "42.gif","43.gif","44.gif","45.gif","46.gif","47.gif","48.gif","49.gif",
             "50.gif","51.gif","52.gif"]

window_icon = "game_icon.ico"

class Cardgame:   #This is the class where whole game runs
    def __init__(self):
        self.__window = Tk()
        self.__window.title("{:d} of a kind".format(ROWS_AND_COLUMNS))
        self.__window.resizable(width=False,height=False)

        #Didn't know if I can return .ico files so i made this exception to
        #make the code work without it.
        try:
            self.__window.iconbitmap(window_icon)
        except:
            pass

        self.__turn = 0
        self.__player_points = [0]*PLAYER_NUMBER
        self.__goal_score = GOAL_SCORE

        self.__number_of_decks = int(ROWS_AND_COLUMNS*ROWS_AND_COLUMNS)
        self.__values_on_screen = [0]*self.__number_of_decks
        self.__cards_on_screen = [-1]*self.__number_of_decks

        #This list is needed to remember which cards are removed from decks
        self.__decks = []
        for deck in range(self.__number_of_decks):
            self.__decks.append([])
            for card in card_deck:
                card_number = int(card.strip(".gif"))-1
                self.__decks[deck].append(card_number)

        self.__cover = PhotoImage(file=deck_cover)
        self.__cardpics = []
        for card in card_deck:
            pic = PhotoImage(file=card)
            self.__cardpics.append(pic)

        #Frame self.__frame1 is located in left side of the window where player
        #scores are shown
        self.__frame1 = Frame(self.__window)
        self.__frame1.grid(row=1,column=0,sticky=E+W)

        for i in range(PLAYER_NUMBER):
            Label(self.__frame1, text="Player "+str(i+1)+" score:")\
            .grid(row=i,column=0,sticky=E)

        #Frame self.__frame2 is top left in the main window
        #Turn/win info and goal score are shown here
        self.__frame2 = Frame(self.__window)
        self.__frame2.grid(row=0,column=0)
        self.__infolabel = Label(self.__frame2,height=5)
        self.__infolabel.grid(row=0,column=0)
        self.__goallabel = Label(self.__frame2,text="Goal score:\n{:d}"
                                 .format(self.__goal_score))
        self.__goallabel.grid(row=1,column=0)

        self.__pointlabels = []
        for i in range(PLAYER_NUMBER):
            new_label = Label(self.__frame1,text=self.__player_points[i])
            new_label.grid(row=i,column=1,sticky=W)
            self.__pointlabels.append(new_label)

        self.__deckbuttons = []
        button_number = 0
        for row in range(ROWS_AND_COLUMNS):
            for col in range(ROWS_AND_COLUMNS):
                new_button = Button(self.__window, image=self.__cover,
                                    command=lambda x=button_number:
                                    self.draw_a_card(x,True,True))
                new_button.grid(row=row,column=2+col)
                self.__deckbuttons.append(new_button)
                button_number += 1

        #Frame self.__frame3 is top right in main window
        #"New game", "Guide" and "Quit game" are there
        self.__frame3 = Frame(self.__window)
        self.__frame3.grid(row=0,column=ROWS_AND_COLUMNS+2,sticky=N)
        self.__new_game = Button(self.__frame3,text="New game",command=self.initialize_game)
        self.__new_game.grid(row=0,column=0,sticky=W+E+N)
        self.__guide = Button(self.__frame3,text="Guide",command=self.guide)\
            .grid(row=1,column=0,sticky=W+E)
        self.__quit_game = Button(self.__frame3,text="Quit game",command=self.quit_game)\
            .grid(row=2,column=0,sticky=E+W+S)

        #This dict contains values of all the cards. Key is card number and
        #value is the value of that card
        self.__card_values = {}
        for i in range(len(card_deck)):
            if i < 13:
                self.__card_values[i] = int(i+1)
            if 13 <= i < 26:
                card_value = i-12
                self.__card_values[i] = card_value
            if 26 <= i < 39:
                card_value = i-25
                self.__card_values[i] = card_value
            if i >= 39:
                card_value = i-38
                self.__card_values[i] = card_value

        self.update_ui_texts()

    def draw_a_card(self,deck_number,check,click):
        '''
        When a deck button is pressed it calls method draw_a_card which draws
        number in range of deck size until it's not the same it was before
        (see while loop).

        This method is also called in method "player_scores" so it need's to know
        how to act with that, so uses parameters "check" and "click" which are
        True or False.
        '''
        while True:
            number = random.randint(0,len(self.__decks[deck_number])-1)
            if number != self.__cards_on_screen[deck_number]:
                break
        pic = self.__decks[deck_number][number]
        self.__deckbuttons[deck_number].configure(image=self.__cardpics[pic])
        self.__values_on_screen[deck_number] = self.__card_values[pic]
        self.__cards_on_screen[deck_number] = number

        if click:
            self.change_buttons_state(NORMAL)
            self.change_buttons_state(DISABLED,deck_number)

        if check:
            self.check_results()

    def check_results(self):
        '''
        Method check__results checks if any rows, columnns or diagonals have cards
        with same value (the calculation is done in next method called values_same).
        If any of these are same, method stores the row/col number or diagonal
        truth value in a list and adds points to a player. Method also checks if
        player gets the goal score.
        '''
        score = 0
        same_cards = [-1,-1,False,False]  #[rows,columns,diagonal,diagonal]

        for i in range(ROWS_AND_COLUMNS):
            if self.values_same(self.__values_on_screen
                             [0+i*ROWS_AND_COLUMNS:3+i*ROWS_AND_COLUMNS]):
                score += self.__values_on_screen[i*ROWS_AND_COLUMNS]
                same_cards[0] = i

            if self.values_same(self.__values_on_screen[i::ROWS_AND_COLUMNS]):
                score += self.__values_on_screen[i]
                same_cards[1] = i

        if self.values_same(self.__values_on_screen[0::ROWS_AND_COLUMNS+1]):
            score += self.__values_on_screen[0]
            same_cards[2] = True

        last_check = self.__values_on_screen[ROWS_AND_COLUMNS-1::ROWS_AND_COLUMNS-1]
        del(last_check[-1])
        if self.values_same(last_check):
            score += self.__values_on_screen[ROWS_AND_COLUMNS-1]
            same_cards[3] = True

        if score != 0:
            self.__player_points[self.__turn] += score
            self.update_ui_texts()
            if self.__player_points[self.__turn] >= GOAL_SCORE:
                self.change_buttons_state(DISABLED)
                self.__infolabel.configure(text="Player "+str(self.__turn+1)+" won\n with "
                                                +str(self.__player_points[self.__turn])+" points!")
                self.__new_game.configure(state=NORMAL)
            else:
                self.player_scores(same_cards)
        else:
            self.end_turn()

    def values_same(self,values):       #Calculations for check_results method
        return all(x == values[0] != 0 for x in values)

    def player_scores(self,cards):
        '''
        Method gets "cards" as a parameter that is a list which tells what rows,
        columns or diagonals need to be redrawn. Decks that need to be drawn are
        stored in a list decks_to_draw.
        '''
        decks_to_draw = []
        if cards[0] != -1:
            for i in range(ROWS_AND_COLUMNS):
                deck = int(cards[0]*ROWS_AND_COLUMNS+i)
                if deck not in decks_to_draw:
                    decks_to_draw.append(deck)

        if cards[1] != -1:
            for i in range(ROWS_AND_COLUMNS):
                deck = int(cards[1]+i*ROWS_AND_COLUMNS)
                if deck not in decks_to_draw:
                    decks_to_draw.append(deck)

        if cards[2]:
            for i in range(ROWS_AND_COLUMNS):
                deck = i*(ROWS_AND_COLUMNS+1)
                if deck not in decks_to_draw:
                    decks_to_draw.append(deck)

        if cards[3]:
            for i in range(ROWS_AND_COLUMNS):
                deck = (i+1)*(ROWS_AND_COLUMNS-1)
                if deck not in decks_to_draw:
                    decks_to_draw.append(deck)

        #Calling method draw_a_card to draw new cards, some delay added
        self.change_buttons_state(DISABLED)
        self.__window.update()
        time.sleep(1)
        counter = 0
        for deck in decks_to_draw:
            self.__window.update()
            time.sleep(0.5)
            del(self.__decks[deck][self.__cards_on_screen[deck]])
            if len(self.__decks[deck]) == 0:
                self.out_of_cards()
                self.__new_game.configure(state=NORMAL)
                break
            if counter != len(decks_to_draw)-1:
                self.draw_a_card(deck,False,False)
                counter += 1
            else:
                self.change_buttons_state(NORMAL)
                self.draw_a_card(deck,True,False)

    def end_turn(self):
        if self.__turn < PLAYER_NUMBER-1:
            self.__turn += 1
        else:
            self.__turn = 0
        self.update_ui_texts()

    def change_buttons_state(self,buttons_state,*this_only):
        '''
        Method changes the state of one or all buttons depending on *argument.
        If *argument is found in parameters, method will only change one specified
        buttons state. New state is gotten as a parameter.
        '''
        if this_only:
            self.__deckbuttons[this_only[0]].configure(state=buttons_state)
        else:
            for i in range(self.__number_of_decks):
                self.__deckbuttons[i].configure(state=buttons_state)
            self.__new_game.configure(state=buttons_state)

    def out_of_cards(self):
        '''
        If method player_scores calls for this method, some of the decks has
        run out of cards and the game ends.
        '''
        self.change_buttons_state(DISABLED)
        max_points = max(self.__player_points)
        winners = [player for player, points in enumerate(self.__player_points)
                   if points == max_points]
        if len(winners) == 1:
            self.__infolabel.configure(text="Out of cards!\nPlayer "
                                            +str(winners[0]+1)+" won\n with "
                                            +str(self.__player_points[self.__turn])
                                            +" points!")
        else:
            list_of_winners = []
            for winner in sorted(winners):
                list_of_winners.append(str(winner))

            self.__infolabel.configure(text="Out of cards!\nPlayers"
                                            +", ".join(list_of_winners)
                                            +"\nwon with\n"+str(max_points))

    def update_ui_texts(self):
        for i in range(len(self.__pointlabels)):
            self.__pointlabels[i].configure(text=self.__player_points[i])

        self.__infolabel.configure(text="Player "+str(self.__turn+1)+" turn")

    def initialize_game(self):
        '''
        Sets everything as they were when the game started.
        '''
        self.__turn = 0
        self.__player_points = [0]*PLAYER_NUMBER
        self.__values_on_screen = [0]*self.__number_of_decks
        self.__cards_on_screen = [-1]*self.__number_of_decks

        self.__decks = []
        for deck in range(self.__number_of_decks):
            self.__decks.append([])
            for card in card_deck:
                card_number = int(card.strip(".gif"))-1
                self.__decks[deck].append(card_number)

        for button in self.__deckbuttons:
            button.configure(image=self.__cover)

        self.update_ui_texts()
        self.change_buttons_state(NORMAL)

    def guide(self):
        '''
        "Guide" -button calls or this method. A top level window is opened and
        guide.txt file is read and shown in the window.

        Error message appears if the file cannot be found or read.
        '''
        guide_window = Toplevel()
        guide_window.title("Guide")
        try:
            guide_window.iconbitmap(window_icon)
        except:
            pass
        guide_window.resizable(width=False, height=False)

        try:
            self.__textfile = open("guide.txt","r")

            numbers = (self.__number_of_decks, ROWS_AND_COLUMNS, GOAL_SCORE)
            textlabel = Label(guide_window,text=self.__textfile.read().format(*numbers))
            textlabel.grid(row=0,column=0)

        except OSError:
            textlabel = Label(guide_window,text='Error: file "guide.txt" not found')
            textlabel.grid(row=0, column=0)
        except IndexError:
            textlabel = Label(guide_window,text='Error: file cannot be read')
            textlabel.grid(row=0, column=0)

        close_button = Button(guide_window,text="Close",command=guide_window.destroy)
        close_button.grid(row=1,column=0)

    def quit_game(self):
        '''
        Open a top level window and ask if you really want to quit.
        '''
        quit_window = Toplevel()
        quit_window.title("Quit game")
        try:
            quit_window.iconbitmap(window_icon)
        except:
            pass
        quit_window.resizable(width=False, height=False)

        quitgamelabel = Label(quit_window,text="Quit game?")
        quitgamelabel.grid(row=0,column=0,columnspan=2,sticky=E+W,padx=40)

        yesbutton = Button(quit_window,text="Yes",command=self.__window.destroy)
        yesbutton.grid(row=1,column=0,sticky=E+W)
        nobutton = Button(quit_window,text="No",command=quit_window.destroy)
        nobutton.grid(row=1,column=1,sticky=E+W)

    def start(self):
        self.__window.mainloop()


def main():
    ui = Cardgame()
    ui.start()

main()