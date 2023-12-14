import json
import os
from anyio import Path
from core.enums.sprite_type import SpriteType
from injector import inject
from core.map import Map
from core.enums.tile_type import TileType
from core.position import Position
from core.services.log_service import LogService
from core.services.service_base import ServiceBase
from core.services.sprite_service import SpriteService
from settings import Settings


class MapService(ServiceBase):
    @inject
    def __init__(
        self, log_service: LogService, sprite_service: SpriteService, settings: Settings
    ):
        super().__init__(settings)
        self.services.logger = log_service
        self.services.sprite = sprite_service
        self.maps_root = Path(__file__).parents[2] / "assets" / "maps"

        self.maps = None

    def get_map(self, map_name: str):
        """Get a map by name."""
        if self.maps is None:
            self.load_maps()

        return self.maps[map_name]

    def load_maps(self):
        """Load all the maps."""
        maps = {}
        for map_file in os.listdir(self.maps_root):
            map_file = self.maps_root / map_file
            map_name = map_file.stem.split(".")[0]
            maps[map_name] = self.load_map(map_file)
        self.maps = maps

    def load_map(self, map_file: Path) -> Map:
        """Load a map from a file."""
        map = None
        with open(map_file, "r") as f:
            map = Map(**json.load(f))

        map.ground = self.convert_to_layer(TileType.GROUND, map.ground)
        map.road = self.convert_to_layer(TileType.ROAD, map.road)
        map.objects = self.convert_to_layer(TileType.OBJECT, map.objects)
        map.checkpoints = self.convert_to_checkpoints(map.checkpoints)

        return map

    def convert_to_layer(self, tile_type: TileType, layer: list):
        """Convert a layer to a layer with sprites."""
        result = []

        for index, tile_id in enumerate(layer):
            if tile_id == -1:
                continue

            sprite_type = None
            match (tile_type):
                case TileType.GROUND | TileType.ROAD:
                    sprite_type = SpriteType.TILE
                case TileType.OBJECT:
                    sprite_type = SpriteType.OBJECT

            tile = self.services.sprite.get_sprite_from(sprite_type, tile_id)
            tile.position = Position(
                (
                    Settings.MAP_OFFSET + (index % 14) * 128,
                    Settings.MAP_OFFSET + (index // 14) * 128,
                )
            )

            result.append(tile)

        return result

    def convert_to_checkpoints(self, layer: list):
        """Convert a layer to a layer with sprites."""
        checkpoints = {}

        for index, checkpoint_id in enumerate(layer):
            if checkpoint_id == -1:
                continue

            checkpoints[checkpoint_id] = Position(
                (
                    Settings.MAP_OFFSET + (index % 14) * 128,
                    Settings.MAP_OFFSET + (index // 14) * 128,
                )
            )

        return {k: checkpoints[k] for k in sorted(checkpoints)}
