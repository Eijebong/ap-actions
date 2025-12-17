import sys
import os
import unittest

if len(sys.argv) != 2:
    print("Usage: tests.py apworld_name")
    sys.exit(1)


ap_root = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
sys.path.insert(0, ap_root)

from worlds.AutoWorld import AutoWorldRegister
from worlds.Files import AutoPatchRegister
from test.bases import WorldTestBase

def world_name_from_apworld_name(apworld_name):
    for name, world in AutoWorldRegister.world_types.items():
        if world.__module__ == f"worlds.{apworld_name}" or world.__module__.startswith(f"worlds.{apworld_name}."):
            return name

    raise Exception(f"Couldn't find loaded world with world: {apworld_name}")

apworld_name = sys.argv[1]
world_name = world_name_from_apworld_name(apworld_name)

# Shamelessly stolen from https://github.com/Eijebong/Archipelago-yaml-checker
# Unload as many worlds as possible before running tests
loaded_worlds = list(AutoWorldRegister.world_types.keys())
for loaded_world in loaded_worlds:
    # Those 3 worlds are essential to testing, don't unload them. Hopefully in the future ALTTP can get yeeted from here too.
    if loaded_world in ("Test Game", "A Link to the Past", "APQuest"):
        continue

    if loaded_world != world_name:
        del AutoWorldRegister.world_types[loaded_world]

        if loaded_world in AutoPatchRegister.patch_types:
            del AutoPatchRegister.patch_types[loaded_world]


class SkipContext:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return True  # Suppress all exceptions

class FilteredTestCase(unittest.TestCase):
    def subTest(self, msg=None, **params):
        if 'game' in params and params['game'] != world_name:
            return SkipContext()

        return super().subTest(msg, **params)


unittest.TestCase = FilteredTestCase

class WorldTest(WorldTestBase):
    game = world_name


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=1)

    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(WorldTest))
    suite.addTests(unittest.defaultTestLoader.discover("test/general", top_level_dir="."))

    apworld_test_folder = f"worlds/{apworld_name}/test"
    if os.path.isdir(apworld_test_folder):
        suite.addTests(unittest.defaultTestLoader.discover(apworld_test_folder, top_level_dir=".", pattern="[Tt]est*.py"))
    results = runner.run(suite)
    if not results.wasSuccessful():
        sys.exit(1)
