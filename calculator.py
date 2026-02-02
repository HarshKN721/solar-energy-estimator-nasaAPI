def calculate_energy(irradiance, area, efficiency, loss_factor=0.75):
    return irradiance * area * efficiency * loss_factor
