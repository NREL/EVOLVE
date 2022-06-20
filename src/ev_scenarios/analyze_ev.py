## Author: Shibani Ghosh

# Date: 08/25/2020
# Parent - C:\github\BRPL-India-pilot\analyze_ev_v2_test.py
# plots and save's are commented out for Kapil D.

import numpy as np
import pandas as pd
import datetime
import opendssdirect as dss
import os
import random
import logging
from collections import defaultdict
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)
LOG_FORMAT = '%(asctime)s: %(levelname)s: %(message)s'
logging.basicConfig(format=LOG_FORMAT,level='DEBUG')

total_EVs_served = 0  # global variable to count # of EVs served

class EV_Charging_Station_Slot:

    def __init__(self,is_it_fast_charger=False,rated_kW_slot=3.3,transition_time_needed_sec=60,tstep_width_sec=300):
        self.is_fast_charger = is_it_fast_charger
        self.occupied = False
        self.charging_EV = None
        self.rated_kW = rated_kW_slot
        self.max_tstep_needed_for_transition = np.floor(transition_time_needed_sec/tstep_width_sec)
        self.required_transition_time = 0
        self.current_consumption = 0

    def assign_EV_to_Slot(self,incoming_EV):
        self.charging_EV=incoming_EV
        self.occupied = True
        self.current_consumption=self.rated_kW

    def update_Slot(self):
        global total_EVs_served
        if self.occupied:
            self.charging_EV.update_EV_soc(self.is_fast_charger, self.rated_kW)
            self.current_consumption = self.rated_kW
            if self.charging_EV.is_charging_complete():
                self.occupied = False
                total_EVs_served = total_EVs_served + 1
                self.required_transition_time = self.max_tstep_needed_for_transition
                self.charging_EV = None
        else:
            self.current_consumption = 0
            if self.required_transition_time > 0:
                self.required_transition_time -= 1  # decreases transition counter if in the transition phase

    def is_occupied_or_transitioning(self):
        if self.occupied or ((not self.occupied)and(self.required_transition_time>0)):
            return True
        else:
            return False


class EV_Charging_Station:

    def __init__(self, rated_kW_, total_slots=10, tstep_width_sec=300):
        # self.is_fast_charging_station = is_it_fast_charging_station
        self.kW_rating = rated_kW_

        self.tstep_sec = tstep_width_sec
        self.No_of_slots = total_slots
        self.EV_Charging_Slots = list()
        for i in range(self.No_of_slots):
            self.EV_Charging_Slots.append(EV_Charging_Station_Slot(rated_kW_slot=self.kW_rating))
        self.EV_Queue = EV_Charging_Station_Queueing(max_queue_size=total_slots)
        self.total_consumption = 0

    def EV_arrived(self,arriving_EV):
        EV_assigned = False
        for Slot in self.EV_Charging_Slots:
            if not Slot.is_occupied_or_transitioning():
                Slot.assign_EV_to_Slot(arriving_EV)
                EV_assigned = True
                break
        if not EV_assigned:
            EV_assigned = self.EV_Queue.add_EV_to_queue(arriving_EV)
        return EV_assigned

    def update_queue_and_Slots(self):
        self.total_consumption = 0
        for Slot in self.EV_Charging_Slots:
            Slot.update_Slot()
            if not Slot.is_occupied_or_transitioning():
                first_EV_in_queue = self.EV_Queue.pop_first_in_line_waiting_EV()
                if first_EV_in_queue is not None:
                    Slot.assign_EV_to_Slot(first_EV_in_queue)
            self.total_consumption += Slot.current_consumption


class EV_Charging_Station_Queueing:

    def __init__(self, max_queue_size=10):
        self.queue_size=max_queue_size
        self.EV_queue = list()
        self.currently_waiting = 0

    def add_EV_to_queue(self,arrived_EV):
        if self.currently_waiting<self.queue_size:
            self.EV_queue.append(arrived_EV)
            self.currently_waiting += 1
            return True
        else:
            return False

    def pop_first_in_line_waiting_EV(self):
        if self.currently_waiting > 0:
            self.currently_waiting -= 1
            return self.EV_queue.pop(0)
        else:
            return None


class EV_individual:

    def __init__(self, tstep_width_sec = 300, arrival_timepoint=10, initial_soc=20, soc_or_time = 'soc',
                 desired_value=95, fast_pref=True, fill_in_hours = 5.5):
        self.tstep_sec = tstep_width_sec
        self.arrival_time=arrival_timepoint
        self.soc = initial_soc
        self.fill_in_time = fill_in_hours
        self.wants_soc_or_time = soc_or_time
        if self.wants_soc_or_time == 'soc':
            self.desired_soc = desired_value
        elif self.wants_soc_or_time == 'time':
            self.desired_duration = desired_value
        else:
            raise ValueError('EV preference needs to be soc or time')
        self.wants_fast = fast_pref
        self.charging_complete = False

    def update_EV_soc(self, is_fast_charger, charger_kW=3.3):
        rate_of_charging = 0
        charging_kW = 0
        if ~is_fast_charger and charger_kW > 3.3:
            zero_to_100_soc_hour = np.round(5.5/(charger_kW/3.3), 3)
            rate_of_charging = 100 / (zero_to_100_soc_hour * 3600)  #assuming linear model where 0 to 100% fast charging takes 1.8 hours
        else:
            if self.soc <= 25:
                rate_of_charging = 100 / (self.fill_in_time * 3600) #assuming linear model where 0 to 100% charging takes 5.5 hours
                charging_kW = self.soc * 3.3 / 25
            elif self.soc>25 and self.soc<=75:
                rate_of_charging = 100 / (self.fill_in_time * 3600) #assuming linear model where 0 to 100% charging takes 8.5 hours for cars
                charging_kW = 3.3
            elif self.soc>75 and self.soc<=90:
                rate_of_charging = 100 / (self.fill_in_time * 3600) #assuming linear model where 0 to 100% charging takes 6.5 hours for bikes
                charging_kW = 7.3 - (0.8/15)*self.soc
            else:
                rate_of_charging = 100 / (self.fill_in_time * 3600) #assuming linear model where 0 to 100% charging takes 5.5 hours for rickshaw
                charging_kW = 25 - 0.25*self.soc

        self.soc += self.tstep_sec * rate_of_charging
        if self.soc >= 100:
            self.soc = 100
            self.charging_complete = True

        if self.wants_soc_or_time == 'time':
            self.desired_duration -= self.tstep_sec

        return charging_kW

    def is_charging_complete(self):
        if self.wants_soc_or_time == 'soc':
            if self.soc >= self.desired_soc:
                self.charging_complete = True
        else:
            if self.desired_duration <= 0:
                self.charging_complete = True
        return self.charging_complete

def generate_random_EVs(no_of_new_EVs, simulation_tstep_width_sec = 300, day_=0, fillin_EVbatt = 5.5):
    # Generate number of new EVs
    #no_of_new_EVs = np.random.randint(3,size=1)

    # Generate Initial_soc of these EVs
    initial_soc_randomized_lower_range = 5  # in %
    initial_soc_randomized_upper_range = 50  # in %
    arrival_times_randomized_lower_range = 4  # 5 pm?
    arrival_times_randomized_upper_range = 10  # 12 am?

    np.random.seed(no_of_new_EVs*(day_*3 + 1))
    initial_socs = np.random.uniform(initial_soc_randomized_lower_range, initial_soc_randomized_upper_range,
                                     size=no_of_new_EVs)
    np.random.seed(no_of_new_EVs*(day_*20 + 1))
    arrival_times = np.random.uniform(arrival_times_randomized_lower_range*3600/simulation_tstep_width_sec,
                                      arrival_times_randomized_upper_range*3600/simulation_tstep_width_sec,
                                      size=no_of_new_EVs)  #

    # Generate soc/time preference of EV
    soc_or_time_pref_binarys = np.zeros(shape=no_of_new_EVs)
    soc_or_times = list()
    desired_values = list()
    for soc_or_time_pref_binary in soc_or_time_pref_binarys:
        if soc_or_time_pref_binary == 0:
            soc_or_times.append('soc')
            np.random.seed(int(no_of_new_EVs/(len(desired_values) + 1)))  # no_of_new_EVs
            desired_values.append(np.random.randint(80,101,size=1))
        else:
            soc_or_times.append('time')
            np.random.seed(int(no_of_new_EVs / (len(desired_values) + 1)))  # no_of_new_EVs
            desired_values.append(np.random.randint(3, 10, size=1)*simulation_tstep_width_sec)

    # Generate fast charging preference of EV
    fast_pref_binarys = np.zeros(shape=no_of_new_EVs)
    fast_prefs = list()
    for fast_pref_binary in fast_pref_binarys:
        if fast_pref_binary == 0:
            fast_prefs.append(False)
        else:
            fast_prefs.append(True)

    generated_EVs = list()
    for i in range(no_of_new_EVs):
        generated_EVs.append(EV_individual(tstep_width_sec=simulation_tstep_width_sec,
                                           arrival_timepoint=arrival_times[i], initial_soc=initial_socs[i],
                                           soc_or_time=soc_or_times[i], desired_value=desired_values[i],
                                           fast_pref=fast_prefs[i], fill_in_hours=fillin_EVbatt))
    return generated_EVs

def generate_random_EVs_for_station(simulation_tstep_width_sec=300, current_timepoint=5, charger_type_kW=3.3, which_year_=0):
    # Generate number of new EVs
    # no_of_new_EVs = np.random.randint(4,size=1)
    no_of_new_EVs = generate_random_EV_numbers_arriving(simulation_tstep_sec=simulation_tstep_width_sec,
                                               current_timepoint_=current_timepoint, charger_kW=charger_type_kW,year_=which_year_)
    # Generate Initial_soc of these EVs

    initial_socs = generate_random_initial_socs(simulation_tstep_sec=simulation_tstep_width_sec,
                                                current_timepoint_=current_timepoint, how_many_EVs=no_of_new_EVs)
    #np.random.uniform(5,50,size=no_of_new_EVs)

    # Generate soc/time preference of EV
    soc_or_time_pref_binarys = np.random.randint(2, size=no_of_new_EVs)
    soc_or_times = list()
    desired_values = list()
    for soc_or_time_pref_binary in soc_or_time_pref_binarys:
        if soc_or_time_pref_binary == 0: #and type_ != 'public_dc50':
            soc_or_times.append('soc')
            min_desired = 60
            max_desired = 85
            if 3600*6 <= current_timepoint*simulation_tstep_width_sec < 3600*8:
                min_desired = 50
                max_desired = 65
            elif 3600*19 <= current_timepoint*simulation_tstep_width_sec < 3600*22:
                min_desired = 70
                max_desired = 100

            desired_values.append(np.random.randint(min_desired,max_desired + 1,size=1))
        else:
            soc_or_times.append('time')
            if charger_type_kW == 50:
                min_desired = 600
                max_desired = 1200
            else:
                min_desired = 900  # seconds
                max_desired = 3000
                if 3600 * 6 <= current_timepoint * simulation_tstep_width_sec < 3600 * 8:
                    min_desired = 900
                    max_desired = 2400
                elif 3600 * 19 <= current_timepoint * simulation_tstep_width_sec < 3600 * 22:
                    min_desired = 900
                    max_desired = 3900

            desired_values.append(np.random.randint(int(np.floor(min_desired/simulation_tstep_width_sec)),
                                                    int(np.floor(max_desired/simulation_tstep_width_sec)),
                                                             size=1)*simulation_tstep_width_sec)

    # Generate fast charging preference of EV
    fast_pref_binarys = np.random.randint(2, size=no_of_new_EVs)
    fast_prefs = list()
    for fast_pref_binary in fast_pref_binarys:
        if fast_pref_binary == 0:
            fast_prefs.append(False)
        else:
            fast_prefs.append(True)

    generated_EVs = list()
    for i in range(no_of_new_EVs[0]):
        generated_EVs.append(EV_individual(tstep_width_sec=simulation_tstep_width_sec,
                                           arrival_timepoint=current_timepoint, initial_soc=initial_socs[i],
                                           soc_or_time=soc_or_times[i], desired_value=desired_values[i],
                                           fast_pref=fast_prefs[i]))
    return generated_EVs


def generate_random_initial_socs(simulation_tstep_sec=300, current_timepoint_=5, how_many_EVs=2):
    min_soc_range = 5
    max_soc_range = 20
    if 0 <= current_timepoint_*simulation_tstep_sec < 3600*3:
        min_soc_range = 5
        max_soc_range = 25
    elif 3600*3 <= current_timepoint_*simulation_tstep_sec < 3600*6:
        min_soc_range = 15
        max_soc_range = 25
    elif 3600*6 <= current_timepoint_*simulation_tstep_sec < 3600*8:
        min_soc_range = 20
        max_soc_range = 25
    elif 3600 * 8 <= current_timepoint_ * simulation_tstep_sec < 3600 * 10:
        min_soc_range = 15
        max_soc_range = 30
    elif 3600 * 10 <= current_timepoint_ * simulation_tstep_sec < 3600 * 12:
        min_soc_range = 30
        max_soc_range = 40
    elif 3600 * 15 <= current_timepoint_ * simulation_tstep_sec < 3600 * 17:
        min_soc_range = 25
        max_soc_range = 45
    elif 3600 * 19 <= current_timepoint_ * simulation_tstep_sec < 3600 * 22:
        min_soc_range = 5
        max_soc_range = 25

    initial_socs_ = np.random.randint(min_soc_range,max_soc_range+1,size=how_many_EVs)
    return initial_socs_

def generate_random_EV_numbers_arriving(simulation_tstep_sec=300, current_timepoint_=5, charger_kW=3.3, year_=0):
    min_ = 0
    max_ = 2
    if charger_kW == 3.3:  # for a station that has about 30 slots
        min_EVs = [0, 2, 6, 4, 2, 5, 6]
        max_EVs = [2, 4, 11, 7, 5, 9, 12]
    elif charger_kW == 15:  # for a station that has about 20 slots --> ~470 EVs
        min_EVs = [0, 1, 10, 2, 2, 4, 5]
        max_EVs = [3, 8, 16, 6, 7, 17, 22]
    elif charger_kW == 10:  # for a station that has about 10 slots  --> ~260 EVs
        min_EVs = [0, 1, 3, 1, 1, 3, 4]
        max_EVs = [2, 3, 8, 3, 8, 10, 12]
    elif charger_kW == 50:  # for a station that has about 5 slots --> ~400 EVs
        min_EVs = [0, 3, 5, 7, 5, 6, 6]
        max_EVs = [4, 5, 10, 9, 8, 10, 12]
    elif charger_kW == 22:  # for a station that has about 15 slots --> ~350 EVs
        min_EVs = [0, 1, 2, 2, 1, 2, 3]
        max_EVs = [2, 3, 4, 3, 3, 5, 6]  # original - BRPL pilot work
        max_EVs = [3, 6, 12, 4, 5, 11, 16]  # modified - high EV, BYPL, 06/03/2020
    else:  # for a station that has about 20 comm ac slots
        # min_EVs = [0, 1, 4, 3, 1, 2, 5]
        # max_EVs = [2, 3, 7, 6, 3, 6, 8]
        min_EVs = [5, 4, 0, 1, 0, 3, 7]  # test to add overnights
        max_EVs = [9, 6, 2, 3, 1, 5, 11]
    # 1 station each type ==> ~1500 EVs a day, i.e. ~2300 e-rickshaws, e-cars, e-bikes etc.
    # (1.55 times of total EVs served)

    if 0 <= current_timepoint_*simulation_tstep_sec < 3600*3:
        min_ = min_EVs[0]
        max_ = max_EVs[0]
    elif 3600*3 <= current_timepoint_*simulation_tstep_sec < 3600*6:
        min_ = min_EVs[1]
        max_ = max_EVs[1]
    elif 3600*6 <= current_timepoint_*simulation_tstep_sec < 3600*8:
        min_ = min_EVs[2]
        max_ = max_EVs[2]
    elif 3600 * 8 <= current_timepoint_ * simulation_tstep_sec < 3600 * 10:
        min_ = min_EVs[3]
        max_ = max_EVs[3]
    elif 3600 * 10 <= current_timepoint_ * simulation_tstep_sec < 3600 * 14:
        min_ = min_EVs[4]
        max_ = max_EVs[4]
    elif 3600 * 14 <= current_timepoint_ * simulation_tstep_sec < 3600 * 18:
        min_ = min_EVs[5]
        max_ = max_EVs[5]
    elif 3600 * 19 <= current_timepoint_ * simulation_tstep_sec < 3600 * 22:
        min_ = min_EVs[6]
        max_ = max_EVs[6]
    # if 0 <= year_ <= 1:
    #     min_ = np.min([(int(min_/5) + 1), min_])
    #     max_= int(max_ / 5) + 2
    # elif 2 <= year_ <= :
    min_ = np.min([(int((year_ + 1)*min_/10) + 1), min_])
    max_ = int((year_ + 1)*max_/10) + 2
    no_of_EVs_ = np.random.randint(min_, max_, size=1)
    return no_of_EVs_


def ev_profile(number_of_evs=300, adoption_percentage=12, res_percentage=100, number_of_days=365):
    #Inputs
    res_percentage = int(res_percentage)
    initial_year_number_of_EVs = number_of_evs
    yearly_increment_percent = adoption_percentage  ## 10 for low, 26 for high EVs- ~2500 at 10th year
    number_of_years = 2
    no_of_residential_chargers = 100
    system_tstep_width_sec = 300
    no_of_days = number_of_days
    timearray = range(int(24*60/5))  #  evaluated every 5 mins

    number_of_EV_in_a_year = list()
    number_of_EV_in_a_year.append(initial_year_number_of_EVs)
    for year_ in range(1, number_of_years):
        number_of_EV_in_a_year.append(int(number_of_EV_in_a_year[year_-1]*(1+yearly_increment_percent/100)))

    no_of_EVs_to_consider = number_of_EV_in_a_year[number_of_years - 1]
    no_of_Res_EVs_to_consider = int(no_of_EVs_to_consider * res_percentage / 100)
    no_of_nonRes_EVs_to_consider = no_of_EVs_to_consider - no_of_Res_EVs_to_consider

    types_of_all_stations = ['public_dc50', 'pvt_ac22', 'govt_dc15', 'capt_ac10']
    kw_of_station = {'public_dc50': 50, 'govt_dc15': 15, 'capt_ac10': 10, 'pvt_ac22': 22}
    total_slots_station = {'public_dc50': 5, 'pvt_ac22': 15, 'govt_dc15': 20, 'capt_ac10': 10}

    #print(number_of_EV_in_a_year)
    # EV_Residential_locations = random.sample(range(no_of_residential_chargers), number_of_EV_in_a_year[-1])

    ## FOR RESIDENTIAL
    consumption_profile = list()

    for i in range(no_of_Res_EVs_to_consider):
        consumption_profile.append(np.zeros(shape=int(24*no_of_days*60/5)))

    no_of_e_rickshaws = int(no_of_Res_EVs_to_consider * 0.7)  # 0.7
    no_of_e_bikes = int(no_of_Res_EVs_to_consider * 0.2)      # 0.2
    no_of_e_cars = no_of_Res_EVs_to_consider - (no_of_e_bikes + no_of_e_rickshaws)

    # for e-rickshaw everyday charging
    for day_ in range(0, no_of_days, 1):
        # print('--- getting data for e-rickshaws ---')
        # print(day_)
        if day_%30 ==0: logging.info(f"Getting data for e-rickshaws for a day {day_}")
        random_EVs = generate_random_EVs(no_of_new_EVs=no_of_e_rickshaws,
                                         simulation_tstep_width_sec=system_tstep_width_sec, day_=day_, fillin_EVbatt=5.5)
        for current_timestep in timearray:
            for EV_no in range(no_of_e_rickshaws):
                current_EV = random_EVs[EV_no]
                if current_timestep > current_EV.arrival_time and not current_EV.is_charging_complete():
                    consumption_profile[EV_no][int(day_*24*60/5+current_timestep)] = current_EV.update_EV_soc(is_fast_charger=False)

    # for e-bikes every alternate day charging
    for day_ in range(0, no_of_days, 2):  # 2
        # print('--- getting data for e-bikes ---')
        # print(day_)
        if day_%30 ==0: logging.info(f"Getting data for e-bikes for a day {day_}")
        random_EVs = generate_random_EVs(no_of_new_EVs=no_of_e_bikes, simulation_tstep_width_sec=system_tstep_width_sec,
                                         day_=day_, fillin_EVbatt=6.5)
        for current_timestep in timearray:
            for EV_no in range(no_of_e_bikes):
                current_EV = random_EVs[EV_no]
                np.random.seed(EV_no*(day_ + 1))
                random_day_on = np.random.randint(0, 3, size=1)
                if random_day_on:
                    if current_timestep > current_EV.arrival_time and not current_EV.is_charging_complete():
                        consumption_profile[EV_no + no_of_e_rickshaws][int(day_*24*60/5+current_timestep)] = \
                            current_EV.update_EV_soc(is_fast_charger=False)

    # for e-car every 4th day charging
    for day_ in range(0, no_of_days, 3):  # 3
        # print('--- getting data for e-cars ---')
        # print(day_)
        if day_%30 ==0: logging.info(f"Getting data for e-cars for a day {day_}")
        random_EVs = generate_random_EVs(no_of_new_EVs=no_of_e_cars, simulation_tstep_width_sec=system_tstep_width_sec,
                                         day_=day_, fillin_EVbatt=8.5)
        for current_timestep in timearray:
            for EV_no in range(no_of_e_cars):
                current_EV = random_EVs[EV_no]
                np.random.seed((EV_no * 2) * (day_ + 1))
                random_day_off = np.random.randint(0, 4, size=1)
                if (random_day_off - 1):
                    if current_timestep > current_EV.arrival_time and not current_EV.is_charging_complete():
                        consumption_profile[EV_no + no_of_e_rickshaws + no_of_e_bikes][int(day_*24*60/5
                                                                                           + current_timestep)] = \
                            current_EV.update_EV_soc(is_fast_charger=False)

    for i_EV in range(no_of_e_rickshaws, no_of_e_rickshaws + no_of_e_bikes):
        day_roll = np.random.randint(2,size=1)
        consumption_profile[i_EV] = np.roll(np.asarray(consumption_profile[i_EV]), 288 * day_roll)

    for i_EV in range(no_of_e_rickshaws + no_of_e_bikes, no_of_e_rickshaws + no_of_e_bikes + no_of_e_cars):
        day_roll = np.random.randint(1,4, size=1)
        consumption_profile[i_EV] = np.roll(np.asarray(consumption_profile[i_EV]), 288 * day_roll)

    # plt.figure(1)
    # timearray = range(int(24 * no_of_days * 60 / 5))
    # plt.plot(timearray,consumption_profile[150][range(int(24*no_of_days*60/5))], 'bo-')
    # plt.plot(timearray,consumption_profile[297][range(int(24*no_of_days*60/5))], 'r*-')
    # plt.plot(timearray, consumption_profile[333][range(int(24 * no_of_days * 60 / 5))], 'g.-')
    # plt.show()

    # plt.figure(2)
    # # timearray = range(int(24 * no_of_days * 60 / 5))
    # ax1=plt.subplot(311)
    # plt.plot(timearray,consumption_profile[157][range(int(24*no_of_days*60/5))], 'o-')
    # # ax1.set_xticks([0, 8, 16, 24, 32, 40, 48])
    # # ax1.set_xticklabels(['12pm', '12am', '8am', '12pm', '4pm', '8pm', '12am'])
    # plt.grid()
    # ax2 = plt.subplot(312)
    # plt.plot(timearray, consumption_profile[295][range(int(24 * no_of_days * 60 / 5))], 'ro-')
    # ax3 = plt.subplot(313)
    # plt.plot(timearray, consumption_profile[330][range(int(24 * no_of_days * 60 / 5))], 'go-')
    # plt.show()

    EV_multi_year_consumption = list()
    for EV_index_ in range(no_of_Res_EVs_to_consider):
        This_EV_multi_year = None
        This_EV_consumption_profile_30min = np.mean(np.reshape(consumption_profile[EV_index_], (96*no_of_days,int(0.25*3600/system_tstep_width_sec))).T, axis=0)
        if EV_index_ > number_of_EV_in_a_year[0]-1:
            This_EV_multi_year = (np.zeros(shape=int(24*no_of_days*60/30)))
        else:
            This_EV_multi_year = This_EV_consumption_profile_30min
        for i in range(1,number_of_years):
            if EV_index_ > number_of_EV_in_a_year[i]-1:
                This_EV_multi_year = np.concatenate([This_EV_multi_year,(np.zeros(shape=int(24*no_of_days*60/30)))])
            else:
                This_EV_multi_year = np.concatenate([This_EV_multi_year,This_EV_consumption_profile_30min])
        EV_multi_year_consumption.append(This_EV_multi_year)
        # load_name = data_possible_EV_loads[EV_Residential_locations[EV_index_]]['name']
        # np.savetxt((res_folder2 + load_name + '_EV.csv'), np.roll(EV_multi_year_consumption[EV_index_],24), fmt='%4.4f', delimiter=",")
        # plt.figure(EV_index_+2)
        # plt.plot(EV_multi_year_consumption[EV_index_])


    multi_year_total_consumption = list()

    for year_ in range(number_of_years):
        if year_ == number_of_years - 1:
            random_mults = np.random.uniform(0.7,0.99, size=no_of_days)
            year_of_interest = np.reshape(sum(consumption_profile[0:(number_of_EV_in_a_year[year_] - 1)]),(no_of_days,288))
            for day_ in range(no_of_days):
                year_of_interest[day_,:] *= random_mults[day_]

        multi_year_total_consumption.extend(sum(consumption_profile[0:(number_of_EV_in_a_year[year_]-1)]))
    This_year_total_consumption_res = multi_year_total_consumption[288 * no_of_days:len(multi_year_total_consumption)]
    This_year_total_consumption_res_30min = np.roll((np.mean(np.reshape(This_year_total_consumption_res,
                                        (96 * no_of_days, int(0.25 * 3600 / system_tstep_width_sec))).T, axis=0)), 24)

    sum_of_all_stations_profile = 0
    factor_to_divide = 1
    # FOR CHARGING STATIONs
    if res_percentage < 100:
        all_station_serving_EV_counts = []
        all_station_profiles = list()
        all_station_no_of_EVs_served = list()
        for type_station in types_of_all_stations:
            all_station_profiles.append(list())
            all_station_no_of_EVs_served.append(list())

        i_station = 0
        daily_EVs_served_station_prev = 0

        for type_station in types_of_all_stations:
            #station_load_name.append(data_large_loads[i_station - 1]["name"])
            # print('Starting Station No:' + str(i_station))
            consumption_profile_station = list()
            incoming_EVs = list()
            wait_list_len = list()
            avg_initial_soc_of_new_EVs = list()
            total_no_EVs_served = list()
            total_no_EVs_served_save = list()

            # Station = genEVshape.EV_Charging_Station(tstep_width_sec=system_tstep_width_sec,
            #                                          is_it_fast_charging_station=dc_station[i_station_count],
            #                                             total_slots=total_slots_stat[i_station_count])

            Station = EV_Charging_Station(tstep_width_sec=system_tstep_width_sec,
                                                     rated_kW_=kw_of_station[type_station],
                                                        total_slots=total_slots_station[type_station])
            daily_EVs_served = 0
            for day_ in range(no_of_days):
                for current_timestep in timearray:

                    Station.update_queue_and_Slots()
                    if np.divmod(current_timestep, 4)[1] == 0:  # every 20 mins
                        EVs_arrived = generate_random_EVs_for_station(simulation_tstep_width_sec=system_tstep_width_sec,
                                                  current_timepoint=current_timestep, charger_type_kW=Station.kW_rating,
                                                                      which_year_=9)
                        temp_init_socs = list()
                        for EV_ in EVs_arrived:
                            Station.EV_arrived(EV_)
                            if len(EVs_arrived) > 0:
                                temp_init_socs.append(EV_.soc)
                        incoming_EVs.append(len(EVs_arrived))
                        if len(EVs_arrived) > 0:
                            avg_initial_soc_of_new_EVs.append(np.mean(temp_init_socs))
                        else:
                            avg_initial_soc_of_new_EVs.append(0)
                    else:
                        incoming_EVs.append(0)
                        avg_initial_soc_of_new_EVs.append(0)
                    wait_list_len.append(Station.EV_Queue.currently_waiting)

                    consumption_profile_station.append(Station.total_consumption)
                # if i_station == 0:

                daily_EVs_served=total_EVs_served - np.sum(total_no_EVs_served)
                # if day_ == 0:
                #     total_no_EVs_served.append(daily_EVs_served - daily_EVs_served_station_prev)
                # else:
                total_no_EVs_served.append(daily_EVs_served)
                total_no_EVs_served_save.append(daily_EVs_served)
                if day_ == no_of_days - 1:
                    if i_station > 0:
                        total_no_EVs_served_save[0] = total_no_EVs_served[0] - daily_EVs_served_station_prev
                    daily_EVs_served_station_prev = np.sum(total_no_EVs_served)


            all_station_no_of_EVs_served[i_station].extend(total_no_EVs_served_save)  #total_no_EVs_served[1:]
            all_station_profiles[i_station].extend(np.mean(np.reshape(consumption_profile_station, (96*no_of_days, int(0.25*3600/system_tstep_width_sec))).T, axis=0))

            i_station = i_station + 1

        sum_of_all_stations_profile = np.sum(all_station_profiles, axis=0)
        avg_EVs_served_all_stations = np.mean(np.sum(np.asarray(all_station_no_of_EVs_served), axis=0))

        # print(no_of_nonRes_EVs_to_consider)
        # print(avg_EVs_served_all_stations)
        # factor_to_divide = avg_EVs_served_all_stations * 1.0 /no_of_nonRes_EVs_to_consider   # 1.5 considers other vehicles that dont charge everyday
        #
        # plt.figure()
        # ax1=plt.subplot(311)
        # plt.plot(sum_of_all_stations_profile/factor_to_divide, '.-')
        # ax1.title.set_text('Stations')
        #
        # ax2=plt.subplot(312)
        # plt.plot((This_year_total_consumption_res_30min + (sum_of_all_stations_profile / factor_to_divide)), 'r.-')
        # ax2.title.set_text('All')
        #
        # ax3 = plt.subplot(313)
        # plt.plot(This_year_total_consumption_res_30min, 'k.-')
        # ax3.title.set_text('Res')
        # plt.show()

        # plt.figure()
        # plt.plot(all_station_no_of_EVs_served,'r.-')
        # plt.show()
    This_year_total_consumption_all_30min = This_year_total_consumption_res_30min + \
                                            (sum_of_all_stations_profile / factor_to_divide)

    # res_folder_ = 'C:\\github\\BRPL-India-pilot\\Results\\for BYPL\\'
    # filename_ = 'EVs_' + str(no_of_EVs_to_consider) + '_res_' + str(res_percentage) + '_net_30min.csv'
    # np.savetxt((res_folder_ + filename_), This_year_total_consumption_all_30min, fmt='%4.4f',
    #            delimiter=",")
    print('-------')
    print(This_year_total_consumption_all_30min)
    return This_year_total_consumption_all_30min   #  This_year_total_consumption_res_30min

    # plt.plot(range(len(This_EV_consumption_profile_30min)),This_EV_consumption_profile_30min)
    # plt.show()

    #
    # system_tstep_width_sec = 300
    # timearray = range(int(24*60/5))
    # consumption_profile = list()
    # Station = EV_Charging_Station(tstep_width_sec=system_tstep_width_sec)
    # for current_timestep in timearray:
    #     Station.update_queue_and_Slots()
    #     if np.divmod(current_timestep,6)[1]==0:
    #         EVs_arrived = generate_random_EVs(simulation_tstep_width_sec = system_tstep_width_sec,
    #                                           current_timepoint = current_timestep)
    #         for EV_ in EVs_arrived:
    #             Station.EV_arrived(EV_)
    #
    #     consumption_profile.append(Station.total_consumption)
    #
    # plt.figure(1)
    # plt.plot(timearray,consumption_profile)
    # plt.show()


if __name__ == "__main__":
    profile = ev_profile(number_of_evs=200, adoption_percentage=0, res_percentage=50, number_of_days=10)
