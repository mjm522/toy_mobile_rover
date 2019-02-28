#Tutorial : how to use ThorPy with a pre-existing code - step 1
import pygame, thorpy

DONE, CANCEL, CLICK_QUIT = thorpy.constants.LAUNCH_DONE, thorpy.constants.LAUNCH_CANCEL, thorpy.constants.LAUNCH_CLICK_QUIT

pygame.init()
pygame.key.set_repeat(300, 30)
screen = pygame.display.set_mode((400,400))
screen.fill((255,255,255))
clock = pygame.time.Clock()

pygame.display.flip()

#declaration of some ThorPy elements ...

encoder = thorpy.Clickable.make("Encoder")
ultrasonic = thorpy.Clickable.make("Ultrasonic")

en_inserter_res = thorpy.Inserter.make(name="Resolution ", value="0.5")
en_inserter_range = thorpy.Inserter.make(name="Range ", value="1.")
en_configure_box = thorpy.make_ok_cancel_box(elements=[en_inserter_res, en_inserter_range])

us_inserter_res = thorpy.Inserter.make(name="Resolution ", value="0.5")
us_inserter_range = thorpy.Inserter.make(name="Range ", value="1.")
us_configure_box = thorpy.make_ok_cancel_box(elements=[us_inserter_res, us_inserter_range])


def us_res_reaction(event): #here is all the dynamics of the game
    print event
    value = us_inserter_res.get_value() #get text inserted by player
    us_inserter_res.set_value(value) #wathever happens, we flush the inserter
    us_inserter_res.unblit_and_reblit() #redraw inserter
    try: #try to cast the inserted value as int number
        guess = int(value)
        print "guess \t", guess
    except ValueError: #occurs for example when trying int("some text")
        return

def us_range_reaction(event): #here is all the dynamics of the game
    print event
    value = us_inserter_range.get_value() #get text inserted by player
    us_inserter_range.set_value(value) #wathever happens, we flush the inserter
    us_inserter_range.unblit_and_reblit() #redraw inserter
    try: #try to cast the inserted value as int number
        guess = int(value)
        print "guess \t", guess
    except ValueError: #occurs for example when trying int("some text")
        return

def en_res_reaction(event): #here is all the dynamics of the game
    print event
    value = en_inserter_res.get_value() #get text inserted by player
    en_inserter_res.set_value(value) #wathever happens, we flush the inserter
    en_inserter_res.unblit_and_reblit() #redraw inserter
    try: #try to cast the inserted value as int number
        guess = int(value)
        print "guess \t", guess
    except ValueError: #occurs for example when trying int("some text")
        return

def en_range_reaction(event): #here is all the dynamics of the game
    print event
    value = en_inserter_range.get_value() #get text inserted by player
    en_inserter_range.set_value(value) #wathever happens, we flush the inserter
    en_inserter_range.unblit_and_reblit() #redraw inserter
    try: #try to cast the inserted value as int number
        guess = int(value)
        print "guess \t", guess
    except ValueError: #occurs for example when trying int("some text")
        return


#We declare a Reaction reaction to THORPY_EVENTs with id EVENT_INSERT
us_reaction_res = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                              reac_func=us_res_reaction,
                              event_args={"id":thorpy.constants.EVENT_INSERT,
                                           "el":us_inserter_res})

us_reaction_range = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                              reac_func=us_range_reaction,
                              event_args={"id":thorpy.constants.EVENT_INSERT,
                                           "el":us_inserter_range})

en_reaction_res = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                              reac_func=en_res_reaction,
                              event_args={"id":thorpy.constants.EVENT_INSERT,
                                           "el":en_inserter_res})

en_reaction_range = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                              reac_func=en_range_reaction,
                              event_args={"id":thorpy.constants.EVENT_INSERT,
                                           "el":en_inserter_range})


us_configure_box.add_reaction(us_reaction_res)
us_configure_box.add_reaction(us_reaction_range)
en_configure_box.add_reaction(en_reaction_res)
en_configure_box.add_reaction(en_reaction_range)

thorpy.set_launcher(encoder, en_configure_box)#, click_quit=True)
thorpy.set_launcher(ultrasonic, us_configure_box)#, click_quit=True)

c_button = thorpy.make_button("Configure")
c_button_box = thorpy.make_ok_cancel_box(elements=[encoder, ultrasonic])
thorpy.set_launcher(c_button, c_button_box, click_quit=True)

q_button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)

background = thorpy.Box.make(elements=[c_button, q_button])

thorpy.store(background)

menu = thorpy.Menu(background)
#important : set the screen as surface for all elements
for element in menu.get_population():
    element.surface = screen

background.set_topleft((10,320))
background.blit()
background.update()


playing_game = True
while playing_game:
    clock.tick(45)
    # print menu.get_population()
    for event in pygame.event.get():
        # background.blit()
        menu.react(event) #the menu automatically integrate your elements

pygame.quit()
