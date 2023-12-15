from injector import inject
import pygame
from core.position import Position
from core.services.log_service import LogService
from core.services.service_base import ServiceBase
from settings import Settings


class CollisionService(ServiceBase):
    @inject
    def __init__(self, log_service: LogService, settings: Settings):
        super().__init__(settings)
        self.services.logger = log_service

    def update(self, timedelta, input_state, map, players):
        # Calculate the move of objects that move, such as cars.
        # Calculate them against objects that are not itself.

        # Initialize collisions dictionary
        collisions = {player: [] for player in players}

        # Check collision against other players
        if Settings.PLAYER_TO_PLAYER_COLLISION:
            self.check_players_collision(players, collisions)

        # Check collision against road and objects
        self.check_road_objects_collision(map, players, collisions)

        # After all collisions are checked, move the cars
        for player, collision_objs in collisions.items():
            player.move(timedelta, collision_objs)

    def check_players_collision(self, players, collisions):
        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                sprite_i = players[i].sprite
                mask_i, offset_i = sprite_i.get_mask()
                mask_i =  pygame.mask.from_surface(mask_i)
                pos_i = Position(sprite_i.position + offset_i)
                sprite_j = players[j].sprite
                mask_j, offset_j = sprite_j.get_mask()
                mask_j =  pygame.mask.from_surface(mask_j)
                pos_j = Position(sprite_j.position + offset_j)

                if mask_i.overlap(mask_j, pos_j - pos_i):
                    # Collision detected, add to collisions dict
                    collisions[players[i]].append(players[j])
                    collisions[players[j]].append(players[i])

    def check_road_objects_collision(self, map, players, collisions):
        for player in players:
            for sprite_obj in map.road + map.objects:
                sprite_player = player.sprite
                mask_player, offset_player = sprite_player.get_mask()
                mask_player =  pygame.mask.from_surface(mask_player)
                pos_player = Position(sprite_player.position + offset_player)

                mask_obj, offset_obj = sprite_obj.get_mask()
                mask_obj =  pygame.mask.from_surface(mask_obj)
                pos_obj = Position(sprite_obj.position + offset_obj)

                if mask_player.overlap(mask_obj, pos_obj - pos_player):
                    # Collision detected, add to collisions dict
                    collisions[player].append(sprite_obj)
