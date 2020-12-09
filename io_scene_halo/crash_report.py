import io
import zipfile
import time
import os
import pdb, traceback, sys
from io_scene_halo import config

class CrashReport:
    def __init__(self):
        self.zip_buffer = io.BytesIO()
        self.zfile = zipfile.ZipFile(self.zip_buffer, "w", zipfile.ZIP_DEFLATED)

        self.add_file("readme.txt", 
        f"""Crash report for Halo-Asset-Blender-Development-Toolset
Please create an issue at {config.URL} or email {config.EMAIL}""")

    def add_file(self, name, contents):
        self.zfile.writestr(name, contents)
    def dump(self):
        """Returns the path the file was dumped to"""
        self.zfile.close()
        crash_dir = os.path.expanduser("~\\blender_halo_crashes")
        try:
            os.makedirs(crash_dir)
        except OSError:
            pass
        file_name = f"{crash_dir}\\{int(time.time())}_crash.zip"
        with open(file_name, 'wb') as f:
            f.write(self.zip_buffer.getvalue())
        return file_name

def report_crash():
    info = sys.exc_info()
    traceback.print_exception(info[0], info[1], info[2])
    if config.ENABLE_DEBUGGING:
        pdb.post_mortem(info[2])
    if config.ENABLE_CRASH_REPORT:
        report = CrashReport()
        report.add_file("crash/traceback.txt", traceback.format_exc())
        try:
            for i, (frame, _) in enumerate(traceback.walk_tb(info[2])):
                if i > 2:
                    report.add_file(f"crash/frames/locals_{i}.txt", str(frame.f_locals))
        except:
            pass

        dump_path = report.dump()
        print(f"Dumped crash report to {dump_path}")
        
        

