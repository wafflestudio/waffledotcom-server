import glob
import sys

sys.dont_write_bytecode = True

# Initialize global fixtures.
pytest_plugins = [
    fixture_file.replace("/", ".").replace('\\', ".").replace(".py", "")
    for fixture_file in glob.glob("src/utils/test/fixtures/[!__]*.py")
]
