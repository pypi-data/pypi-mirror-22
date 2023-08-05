import asyncio
import logging

from . import decode_base64

LOGGER = logging.getLogger("__name__")


class Scenes:
    def __init__(self, hub_ip, aio_request):
        self.request = aio_request
        self._scenes_path = "{}/scenes".format(hub_ip)

    @staticmethod
    def sanitize_scenes(scenes):
        """Cleans up incoming scene data

        :param scenes: The dict with scene data to be sanitized.
        :return: Cleaned up scene dict.
        """
        try:
            for scene in scenes['sceneData']:
                scene['name'] = decode_base64(scene['name'])
            return scenes
        except KeyError:
            LOGGER.debug("no scene data available")

    @asyncio.coroutine
    def get_scenes(self):
        """Get alist of scenes.

        :returns: A json object.
        """
        scenes = yield from self.request.get(self._scenes_path)
        return Scenes.sanitize_scenes(scenes)

    @asyncio.coroutine
    def activate_scene(self, scene_id: int):
        """Activate a scene

        :param scene_id: The id of the scene.
        :return: Nothing.
        """
        yield from self.request.get(self._scenes_path, {"sceneid": scene_id})
