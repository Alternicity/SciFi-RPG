#originally this file was generateCity.py, but it seems to run the city logic
#more than generate a city so I deprecated it and renamed it that.

def calculate_worker_needs(locations):
    total_workers_needed = 0
    for location in locations:
        if hasattr(location, 'workers_needed'):
            total_workers_needed += location.workers_needed
    return total_workers_needed
def assign_workers(civilians, locations):
    unassigned_civilians = civilians[:]
    for location in locations:
        if hasattr(location, 'workers_needed'):
            for _ in range(location.workers_needed):
                if unassigned_civilians:
                    worker = unassigned_civilians.pop(0)
                    worker.current_job = location
                    worker.shift = "Day" if len(location.workers) % 2 == 0 else "Night"
                    location.workers.append(worker)
                else:
                    break
def daily_economy(locations):
    for location in locations:
        if hasattr(location, 'workers') and hasattr(location, 'profit'):
            # Pay workers
            for worker in location.workers:
                worker.money += location.worker_pay
                if worker.fun >= 0:
                    worker.loyalty += 1

            # Calculate and pay taxes
            tax = location.profit * 0.1  # Flat 10% tax rate
            location.profit -= tax
            location.taxes_paid += tax
