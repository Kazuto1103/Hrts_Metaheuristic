import json

data = json.load(open('datasets/dataset_bpm_optimized.json'))

print('=== SAMPLE DATA VERIFICATION ===')
print()

# Check orang_1
print('orang_1 (template):')
print(f'  Device ID: {data["orang_1"]["metadata"]["device_id"]}')
print(f'  Location: {data["orang_1"]["metadata"]["measurement_location"]}')
print(f'  Timestamp: {data["orang_1"]["metadata"]["timestamp"]}')
print(f'  First 3 readings:')
for i in range(3):
    r = data['orang_1']['timeline'][i]
    print(f'    sec {r["second"]}: {r["bpm"]} bpm - {r["classification"]} (conf: {r["confidence"]})')
print()

# Check orang_11 (should be similar to orang_1 with slight variation)
print('orang_11 (copy of orang_1 with variation):')
print(f'  Device ID: {data["orang_11"]["metadata"]["device_id"]}')
print(f'  Location: {data["orang_11"]["metadata"]["measurement_location"]}')
print(f'  Timestamp: {data["orang_11"]["metadata"]["timestamp"]}')
print(f'  First 3 readings:')
for i in range(3):
    r = data['orang_11']['timeline'][i]
    print(f'    sec {r["second"]}: {r["bpm"]} bpm - {r["classification"]} (conf: {r["confidence"]})')
print()

# Check orang_21 (should be similar to orang_1)
print('orang_21 (copy of orang_1 with variation):')
print(f'  Device ID: {data["orang_21"]["metadata"]["device_id"]}')
print(f'  Location: {data["orang_21"]["metadata"]["measurement_location"]}')
print(f'  Timestamp: {data["orang_21"]["metadata"]["timestamp"]}')
print(f'  First 3 readings:')
for i in range(3):
    r = data['orang_21']['timeline'][i]
    print(f'    sec {r["second"]}: {r["bpm"]} bpm - {r["classification"]} (conf: {r["confidence"]})')
print()

print('All locations in dataset:')
locations = set()
for person_key, person_data in data.items():
    locations.add(person_data["metadata"]["measurement_location"])
print(f'Unique locations: {locations}')
