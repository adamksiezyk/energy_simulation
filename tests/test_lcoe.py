from energy_simulation.lcoe import EnergySource, calculate_lcoe


def test_onshore_wind_farm():
    es = EnergySource(cost_per_gw=5.4,
                      max_power_perc=0.36,
                      o_and_m_per_gw_per_year=0.065,
                      o_and_m_per_twh=0.007,
                      years_to_launch=2,
                      years_of_operation=25)
    output = calculate_lcoe(es, discount_factor=0.05)
    expected = 152
    assert round(output) == expected


def test_offshore_wind_farm():
    es = EnergySource(cost_per_gw=12.0,
                      max_power_perc=0.5,
                      o_and_m_per_gw_per_year=0.184,
                      o_and_m_per_twh=0.014,
                      years_to_launch=4,
                      years_of_operation=20)
    output = calculate_lcoe(es, discount_factor=0.05)
    expected = 293
    assert round(output) == expected


def test_photovoltaics():
    es = EnergySource(cost_per_gw=2.2,
                      max_power_perc=0.11,
                      o_and_m_per_gw_per_year=0.052,
                      o_and_m_per_twh=0.0,
                      years_to_launch=1,
                      years_of_operation=30)
    output = calculate_lcoe(es, discount_factor=0.05)
    expected = 202
    assert round(output) == expected


def test_nuclear():
    es = EnergySource(cost_per_gw=35,
                      max_power_perc=0.85,
                      o_and_m_per_gw_per_year=0.5,
                      o_and_m_per_twh=0.016,
                      years_to_launch=10,
                      years_of_operation=60)
    output = calculate_lcoe(es, discount_factor=0.05)
    expected = 395
    assert round(output) == expected


def test_gas():
    es = EnergySource(cost_per_gw=4,
                      max_power_perc=0.01859,  # should be 20% originally
                      o_and_m_per_gw_per_year=0.0,
                      o_and_m_per_twh=0.5,
                      years_to_launch=3,
                      years_of_operation=40)
    output = calculate_lcoe(es, discount_factor=0.05)
    expected = 2004
    assert round(output) == expected
