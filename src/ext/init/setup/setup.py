import os, sys
src_dir = f'{os.path.dirname(__file__)}/../..'
from ext import const
from modules import compress


os.chdir(src_dir)
# install required packages
print("==> Installing packages...")
if sys.platform == "linux":
    os.system(f"python3 -m pip install --requirements ../requirement.txt")
print("==> Creating data files and configs...")
f = open(const.LASTWRDFILE, 'w')
f.write("{}")
f.close()
open("data/mcsrvs.csv", 'w+').close()
open("data/pyoutput.txt", 'w+').close()
f = open(const.SETFILE, 'w')
f.write("{}")
f.close()
open("data/warnings.db", 'w+').close()


print("==> Decompressing scripts...")
def write_special():
    scr = compress.decompress("ext/init/setup/special.py.lzma")
    f = open("special.py", 'w+')
    f.write(scr)
    f.close()

if "special.py" in os.listdir():
    if ['y', 'yes'] in input("Do you want to overwrite special.py? (y/N)"):
        write_special()
else:
    write_special()
