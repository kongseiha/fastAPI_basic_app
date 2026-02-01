import os

print("📁 Current directory:", os.getcwd())
print("\n📄 Files in root:")
for f in os.listdir('.'):
    print(f"  - {f}")

print("\n📁 Files in app/")
for f in os.listdir('app'):
    print(f"  - {f}")

print("\n📄 requirements.txt content:")
with open('requirements.txt', 'r') as f:
    print(f.read())