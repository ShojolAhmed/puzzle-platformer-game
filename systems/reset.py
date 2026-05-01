def reset_player(player, spawn):
    player.rect.x, player.rect.y = spawn
    player.vel_x = 0
    player.vel_y = 0
    player.has_key = False