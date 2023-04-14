from io_scene_foundry.utils.nwo_utils import get_ek_path
import sys
import os
import random

packages_path = os.path.join(sys.exec_prefix, 'lib', 'site-packages')
sys.path.append(packages_path)
mb_path = os.path.join(get_ek_path(), 'bin', 'managedblam')

try:
    import clr
    try:
        clr.AddReference(mb_path)
        try:
            import Bungie
        except:
            try:
                import Corinth as Bungie
            except:
                print("Failed to import ManagedBlam module")
    except:
        print('Failed to add reference to ManagedBlam')
except:
    print("Couldn't find clr module")


class ManagedBlam():
    def __init__(self):
        print("init!")
        try:
            startup_parameters = Bungie.ManagedBlamStartupParameters()
            startup_parameters.InitializationLevel = Bungie.InitializationType.TagsOnly
            Bungie.ManagedBlamSystem.Start(get_ek_path(), self.callback(), startup_parameters)
        except:
            print("Was already running...")

        self.new_tag(f"blam\\triple_blam\\a_shader_{random.randint(0, 1000)}.shader")

    def callback(self):
        pass

    def stop(self):
        Bungie.ManagedBlamSystem.Stop()

    def new_tag(self, user_path):
        relative_path, tag_ext = self.get_path_and_ext(user_path)
        new_tag = Bungie.Tags.TagFile()
        new_path = Bungie.Tags.TagPath.FromPathAndExtension(relative_path, tag_ext)
        try:
            new_tag.New(new_path)
            new_tag.Save()

        finally:
            new_tag.Dispose()

    def get_path_and_ext(self, user_path):
        return user_path.rpartition('.')[0], user_path.rpartition('.')[2]