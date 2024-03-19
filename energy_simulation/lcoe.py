import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EnergySource:
    """
    Represents the costs of an energy source
    """
    cost_per_gw: float
    """Cost in arbitrary currency per GW of power"""
    max_power_perc: float
    """Percentage of maximal generator power"""
    o_and_m_per_gw_per_year: float
    """Operation and Maintanance costs of producing 1 GW of power"""
    o_and_m_per_twh: float
    """Operation and Maintanance costs of storing 1 TWh of power"""
    years_to_launch: int
    """Number of years the energy source takes to build"""
    years_of_operation: int
    """Number of years the energy source will operate"""


def calculate_lcoe(energy_source: EnergySource, discount_factor: float) -> float:
    """
    Calculates the Levelized Cost Of Energy.
    """
    twh_of_energy_from_one_gw_per_year = energy_source.max_power_perc * 365 * 24 / 1000

    expenses = []
    energy = []
    discount = 1.0
    for _ in range(energy_source.years_to_launch):
        expenses.append(energy_source.cost_per_gw / energy_source.years_to_launch * discount)
        energy.append(0.0)
        logger.debug(f"Discount: {discount:.2f},\tExpense: {expenses[-1]:.2f},\tEnergy: {energy[-1]:.2f}")
        discount = discount / (1 + discount_factor)
    for _ in range(energy_source.years_of_operation):
        expenses.append(
            (
                energy_source.o_and_m_per_gw_per_year +
                twh_of_energy_from_one_gw_per_year * energy_source.o_and_m_per_twh
            ) *
            discount
        )
        energy.append(twh_of_energy_from_one_gw_per_year * discount)
        logger.debug(f"Discount: {discount:.2f},\tExpense: {expenses[-1]:.2f},\tEnergy: {energy[-1]:.2f}")
        discount = discount / (1 + discount_factor)
    return sum(expenses) / sum(energy) * 1e3
