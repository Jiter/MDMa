# this goes in boot.py not code.py!
new_name = "CIRCUITPYR"
import storage
storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = new_name
storage.remount("/", readonly=True)

