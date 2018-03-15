shoot_sound = pg.mixer.Sound(os.path.join(snd_folder, 'Laser_Shoot2.wav'))
player_die_sound = pg.mixer.Sound(os.path.join(snd_folder, 'rumble1.ogg'))
player_hit = pg.mixer.Sound(os.path.join(snd_folder, 'Explosion_hit.wav'))
expl_sounds = []
for snd in ['Explosion_met1.wav', 'Explosion_met2.wav']:
    expl_sounds.append(pg.mixer.Sound(os.path.join(snd_folder, snd)))
