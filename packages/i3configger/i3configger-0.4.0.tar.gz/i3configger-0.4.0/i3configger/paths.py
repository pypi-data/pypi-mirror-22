import logging
import os
from pathlib import Path

from i3configger import config, exc

log = logging.getLogger(__name__)

MY_CONFIG_NAME = 'i3configger.json'
STATE_FILE_NAME = '.state.json'
MY_CONFIG_FOLDER = 'config.d'
MY_REL_CONFIG_PATH = MY_CONFIG_FOLDER + '/' + MY_CONFIG_NAME


class Paths:
    def __init__(self, configPath):
        path = Path(configPath)
        assert path.exists() and path.is_file(), path
        self.root = path.parent
        self.config = configPath
        self.state = self.root / STATE_FILE_NAME


def get_my_config_path(configPath=None):
    if not configPath:
        i3configPath = get_i3_config_path()
        configContainer = i3configPath / MY_CONFIG_FOLDER
        if not configContainer.exists():
            log.info("create new config folder at %s", configContainer)
            configContainer.mkdir()
        configPath = configContainer / MY_CONFIG_NAME
    elif configPath.is_dir():
            configPath /= MY_CONFIG_NAME
    if not configPath.exists():
        log.info("create default configuration at %s", configPath)
        config.freeze(configPath, config.I3_CONFIGGER_DEFAULTS)
    return configPath


def get_i3_config_path():
    """Use same search order like i3 (no system stuff though).

    see: https://github.com/i3/i3/blob/4.13/libi3/get_config_path.c#L31
    """
    candidates = [
        Path('~/.i3').expanduser(),
        Path(os.getenv("XDG_CONFIG_HOME", '~/.config/')).expanduser() / 'i3']
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise exc.ConfigError(
        f"can't find i3 config at the standard locations: {candidates}")
