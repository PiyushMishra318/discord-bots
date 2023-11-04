import subprocess

# Start Bot 1
subprocess.Popen(["python", "server/oso_bot.py"])

# Start Bot 2
subprocess.Popen(["python", "server/casual_bot.py"])

# Start Bot 3
subprocess.Popen(["python", "server/kakashi_bot.py"])

