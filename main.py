from pico2d import open_canvas, close_canvas

import game_framework
import title_mode as start_mode
# import select_mode as start_mode
# import play_mode as start_mode
open_canvas()
game_framework.run(start_mode)
close_canvas()
