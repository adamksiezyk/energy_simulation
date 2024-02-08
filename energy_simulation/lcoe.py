import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@dataclass
class EnergySource:
    """
    Represents the costs of an energy source
    """
    cost_per_gw: float
    twh_per_gw_per_year: float
    o_and_m_per_gw_per_year: float
    o_and_m_per_twh: float


def calculate_lcoe(energy_source: EnergySource,
                   years_to_launch: int,
                   years_of_operation: int,
                   discount_factor: float) -> float:
    """
    Calculates the Levelized Cost Of Energy.
    """
    expenses = []
    energy = []
    discount = 1.0
    for _ in range(years_to_launch):
        expenses.append(energy_source.cost_per_gw / years_to_launch * discount)
        energy.append(0.0)
        logger.debug(f"Discount: {discount:.2f},\tExpense: {expenses[-1]:.2f},\tEnergy: {energy[-1]:.2f}")
        discount = discount / (1 + discount_factor)
    for _ in range(years_of_operation):
        expenses.append(
            (energy_source.o_and_m_per_gw_per_year + energy_source.twh_per_gw_per_year * energy_source.o_and_m_per_twh) *
            discount
        )
        energy.append(energy_source.twh_per_gw_per_year * discount)
        logger.debug(f"Discount: {discount:.2f},\tExpense: {expenses[-1]:.2f},\tEnergy: {energy[-1]:.2f}")
        discount = discount / (1 + discount_factor)
    return sum(expenses) / sum(energy) * 1e3


if __name__ == "__main__":
    # Onshore wind farm
    max_power = 0.36
    es = EnergySource(cost_per_gw=5.4,
                      twh_per_gw_per_year=(max_power * 365 * 24 / 1000),
                      o_and_m_per_gw_per_year=0.065,
                      o_and_m_per_twh=0.007)
    lcoe = calculate_lcoe(es,
                          years_to_launch=2,
                          years_of_operation=25,
                          discount_factor=0.05)
    logger.info(f"LCOE = {lcoe:.2f} [PLN/MWh]")
