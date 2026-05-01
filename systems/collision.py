def is_on_platform(player, platform):
    test_rect = player.rect.copy()
    test_rect.y += 2
    return test_rect.colliderect(platform.rect)