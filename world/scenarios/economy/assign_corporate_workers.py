#world.scenarios.economy.assign_corporate_workers.py

def assign_corporate_workers(corp):
    #single corp logic
    from augment.augment_corporations import assign_factory_workers, assign_power_workers
    
    
    assign_power_workers(corp)
    assign_factory_workers(corp)
    