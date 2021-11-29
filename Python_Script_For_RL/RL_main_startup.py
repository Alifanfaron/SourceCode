import numpy as np
import pandas as pd
import time
import sys
from datetime import datetime

trainingStepPerEpisode = 500
MAX_EPISODES = 100  # maximum episodes

WakeupDuration = 120000
DeepsleepDuration = 1500000

sensorPhase_2 = 982500
sensorPhase_3 = 612500
sensorPhase_4 = 365000
sensorPhase_5 = 625000
sensorPhase_6 = 865000
sensorPhase_7 = 1315000
sensorPhase_8 = 872500
sensorPhase_9 = 1480000
sensorPhase_10 = 1030000

np.random.seed(8)  # reproducible

WakeupEnergyCostPerHourPercentage = 0.024668
DeepsleepEnergyCostPerHourPercentage = 0.003289
WakeupFromD0FunctionEnergyCostPerHourPercentage = 0.0013266
RewardMarkOfSpotIgnitionTimeForEvery1Percent = -1000.0
RewardMarkOfSensorLifespanForEvery1Percent = 1900.0
RewardMarkOfActionPenalty = -1.0
EPSILON = 0.9  # greedy police
ALPHA = 0.1  # learning rate
GAMMA = 0.9  # discount factor
FRESH_TIME = 0.0000005  # fresh time for one move
RangeOfAdjust = 15000

ACTIONS = ['S2_phase_plus', 'S3_phase_plus', 'S4_phase_plus', 'S5_phase_plus', 'S6_phase_plus',
           'S7_phase_plus', 'S8_phase_plus', 'S9_phase_plus', 'S10_phase_plus',
           'S2_phase_minus', 'S3_phase_minus', 'S4_phase_minus', 'S5_phase_minus', 'S6_phase_minus',
           'S7_phase_minus', 'S8_phase_minus', 'S9_phase_minus', 'S10_phase_minus',
           'WakeupDuration_plus', 'WakeupDuration_minus',
           'DeepsleepDuration_plus', 'DeepsleepDuration_minus',
           'NoAction'
           ]  # available actions

WakeupDuration_0 = WakeupDuration
DeepsleepDuration_0 = DeepsleepDuration
sensorPhase_2_0 = sensorPhase_2
sensorPhase_3_0 = sensorPhase_3
sensorPhase_4_0 = sensorPhase_4
sensorPhase_5_0 = sensorPhase_5
sensorPhase_6_0 = sensorPhase_6
sensorPhase_7_0 = sensorPhase_7
sensorPhase_8_0 = sensorPhase_8
sensorPhase_9_0 = sensorPhase_9
sensorPhase_10_0 = sensorPhase_10

N_STATES = 5 + trainingStepPerEpisode  # the lines of the Q-table


def resetGlobalParametersBackToDefaultValue():
    global WakeupDuration, DeepsleepDuration, sensorPhase_2, sensorPhase_3, sensorPhase_4, sensorPhase_5, sensorPhase_6, sensorPhase_7, sensorPhase_8, sensorPhase_9, sensorPhase_10
    WakeupDuration = WakeupDuration_0
    DeepsleepDuration = DeepsleepDuration_0
    sensorPhase_2 = sensorPhase_2_0
    sensorPhase_3 = sensorPhase_3_0
    sensorPhase_4 = sensorPhase_4_0
    sensorPhase_5 = sensorPhase_5_0
    sensorPhase_6 = sensorPhase_6_0
    sensorPhase_7 = sensorPhase_7_0
    sensorPhase_8 = sensorPhase_8_0
    sensorPhase_9 = sensorPhase_9_0
    sensorPhase_10 = sensorPhase_10_0


def sensorPhase_2_plus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_2
    if sensorPhase_2 + RangeOfAdjust >= Calculation_tmp:
        sensorPhase_2 = (sensorPhase_2 + RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_2 + RangeOfAdjust < 0:
        sensorPhase_2 = (sensorPhase_2 + RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_2 = sensorPhase_2 + RangeOfAdjust


def sensorPhase_3_plus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_3
    if sensorPhase_3 + RangeOfAdjust >= Calculation_tmp:
        sensorPhase_3 = (sensorPhase_3 + RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_3 + RangeOfAdjust < 0:
        sensorPhase_3 = (sensorPhase_3 + RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_3 = sensorPhase_3 + RangeOfAdjust


def sensorPhase_4_plus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_4
    if sensorPhase_4 + RangeOfAdjust >= Calculation_tmp:
        sensorPhase_4 = (sensorPhase_4 + RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_4 + RangeOfAdjust < 0:
        sensorPhase_4 = (sensorPhase_4 + RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_4 = sensorPhase_4 + RangeOfAdjust


def sensorPhase_5_plus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_5
    if sensorPhase_5 + RangeOfAdjust >= Calculation_tmp:
        sensorPhase_5 = (sensorPhase_5 + RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_5 + RangeOfAdjust < 0:
        sensorPhase_5 = (sensorPhase_5 + RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_5 = sensorPhase_5 + RangeOfAdjust


def sensorPhase_6_plus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_6
    if sensorPhase_6 + RangeOfAdjust >= Calculation_tmp:
        sensorPhase_6 = (sensorPhase_6 + RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_6 + RangeOfAdjust < 0:
        sensorPhase_6 = (sensorPhase_6 + RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_6 = sensorPhase_6 + RangeOfAdjust


def sensorPhase_7_plus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_7
    if sensorPhase_7 + RangeOfAdjust >= Calculation_tmp:
        sensorPhase_7 = (sensorPhase_7 + RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_7 + RangeOfAdjust < 0:
        sensorPhase_7 = (sensorPhase_7 + RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_7 = sensorPhase_7 + RangeOfAdjust


def sensorPhase_8_plus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_8
    if sensorPhase_8 + RangeOfAdjust >= Calculation_tmp:
        sensorPhase_8 = (sensorPhase_8 + RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_8 + RangeOfAdjust < 0:
        sensorPhase_8 = (sensorPhase_8 + RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_8 = sensorPhase_8 + RangeOfAdjust


def sensorPhase_9_plus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_9
    if sensorPhase_9 + RangeOfAdjust >= Calculation_tmp:
        sensorPhase_9 = (sensorPhase_9 + RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_9 + RangeOfAdjust < 0:
        sensorPhase_9 = (sensorPhase_9 + RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_9 = sensorPhase_9 + RangeOfAdjust


def sensorPhase_10_plus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_10
    if sensorPhase_10 + RangeOfAdjust >= Calculation_tmp:
        sensorPhase_10 = (sensorPhase_10 + RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_10 + RangeOfAdjust < 0:
        sensorPhase_10 = (sensorPhase_10 + RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_10 = sensorPhase_10 + RangeOfAdjust


def sensorPhase_2_minus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_2
    if sensorPhase_2 - RangeOfAdjust >= Calculation_tmp:
        sensorPhase_2 = (sensorPhase_2 - RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_2 - RangeOfAdjust < 0:
        sensorPhase_2 = (sensorPhase_2 - RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_2 = sensorPhase_2 - RangeOfAdjust


def sensorPhase_3_minus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_3
    if sensorPhase_3 - RangeOfAdjust >= Calculation_tmp:
        sensorPhase_3 = (sensorPhase_3 - RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_3 - RangeOfAdjust < 0:
        sensorPhase_3 = (sensorPhase_3 - RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_3 = sensorPhase_3 - RangeOfAdjust


def sensorPhase_4_minus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_4
    if sensorPhase_4 - RangeOfAdjust >= Calculation_tmp:
        sensorPhase_4 = (sensorPhase_4 - RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_4 - RangeOfAdjust < 0:
        sensorPhase_4 = (sensorPhase_4 - RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_4 = sensorPhase_4 - RangeOfAdjust


def sensorPhase_5_minus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_5
    if sensorPhase_5 - RangeOfAdjust >= Calculation_tmp:
        sensorPhase_5 = (sensorPhase_5 - RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_5 - RangeOfAdjust < 0:
        sensorPhase_5 = (sensorPhase_5 - RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_5 = sensorPhase_5 - RangeOfAdjust


def sensorPhase_6_minus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_6
    if sensorPhase_6 - RangeOfAdjust >= Calculation_tmp:
        sensorPhase_6 = (sensorPhase_6 - RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_6 - RangeOfAdjust < 0:
        sensorPhase_6 = (sensorPhase_6 - RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_6 = sensorPhase_6 - RangeOfAdjust


def sensorPhase_7_minus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_7
    if sensorPhase_7 - RangeOfAdjust >= Calculation_tmp:
        sensorPhase_7 = (sensorPhase_7 - RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_7 - RangeOfAdjust < 0:
        sensorPhase_7 = (sensorPhase_7 - RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_7 = sensorPhase_7 - RangeOfAdjust


def sensorPhase_8_minus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_8
    if sensorPhase_8 - RangeOfAdjust >= Calculation_tmp:
        sensorPhase_8 = (sensorPhase_8 - RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_8 - RangeOfAdjust < 0:
        sensorPhase_8 = (sensorPhase_8 - RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_8 = sensorPhase_8 - RangeOfAdjust


def sensorPhase_9_minus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_9
    if sensorPhase_9 - RangeOfAdjust >= Calculation_tmp:
        sensorPhase_9 = (sensorPhase_9 - RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_9 - RangeOfAdjust < 0:
        sensorPhase_9 = (sensorPhase_9 - RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_9 = sensorPhase_9 - RangeOfAdjust


def sensorPhase_10_minus_Action():
    Calculation_tmp = WakeupDuration + DeepsleepDuration
    global sensorPhase_10
    if sensorPhase_10 - RangeOfAdjust >= Calculation_tmp:
        sensorPhase_10 = (sensorPhase_10 - RangeOfAdjust) - Calculation_tmp
    elif sensorPhase_10 - RangeOfAdjust < 0:
        sensorPhase_10 = (sensorPhase_10 - RangeOfAdjust) + Calculation_tmp
    else:
        sensorPhase_10 = sensorPhase_10 - RangeOfAdjust


def WakeupDuration_plus_Action():
    global WakeupDuration
    WakeupDuration = WakeupDuration + RangeOfAdjust


def WakeupDuration_minus_Action():
    global WakeupDuration
    if (WakeupDuration - RangeOfAdjust) <= 0:
        WakeupDuration = WakeupDuration
    else:
        WakeupDuration = WakeupDuration - RangeOfAdjust


def DeepsleepDuration_plus_Action():
    global DeepsleepDuration
    DeepsleepDuration = DeepsleepDuration + RangeOfAdjust


def DeepsleepDuration_minus_Action():
    global DeepsleepDuration
    if (DeepsleepDuration - RangeOfAdjust) <= 0:
        DeepsleepDuration = WakeupDuration
    else:
        DeepsleepDuration = DeepsleepDuration - RangeOfAdjust


def ResultOfSpotIgnition_Min(WakeupDuration, DeepsleepDuration, sensorPhase_2, sensorPhase_3, sensorPhase_4,
                             sensorPhase_5, sensorPhase_6, sensorPhase_7, sensorPhase_8, sensorPhase_9, sensorPhase_10):
    DutyCycle = WakeupDuration + DeepsleepDuration
    TotalSpotTime = 0
    for ignitionTimer in range(0, 10):
        ignitionTime_tmp = ignitionTimer * DutyCycle / 10
        time_1 = time_2 = time_3 = time_4 = time_5 = time_6 = time_7 = time_8 = time_9 = time_10 = 0
        time_1 = ignitionTime_tmp
        time_2 = ignitionTime_tmp
        if sensorPhase_2 >= ignitionTime_tmp:
            time_3 = sensorPhase_2 - ignitionTime_tmp
        else:
            time_3 = sensorPhase_2 + DutyCycle - ignitionTime_tmp
        if sensorPhase_3 >= ignitionTime_tmp:
            time_4 = sensorPhase_3 - ignitionTime_tmp
        else:
            time_4 = sensorPhase_3 + DutyCycle - ignitionTime_tmp
        if sensorPhase_4 >= ignitionTime_tmp:
            time_5 = sensorPhase_4 - ignitionTime_tmp
        else:
            time_5 = sensorPhase_4 + DutyCycle - ignitionTime_tmp
        if sensorPhase_5 >= ignitionTime_tmp:
            time_6 = sensorPhase_5 - ignitionTime_tmp
        else:
            time_6 = sensorPhase_5 + DutyCycle - ignitionTime_tmp
        if sensorPhase_6 >= ignitionTime_tmp:
            time_7 = sensorPhase_6 - ignitionTime_tmp
        else:
            time_7 = sensorPhase_6 + DutyCycle - ignitionTime_tmp
        if sensorPhase_8 >= ignitionTime_tmp:
            time_8 = sensorPhase_8 - ignitionTime_tmp
        else:
            time_8 = sensorPhase_8 + DutyCycle - ignitionTime_tmp
        if sensorPhase_9 >= ignitionTime_tmp:
            time_9 = sensorPhase_9 - ignitionTime_tmp
        else:
            time_9 = sensorPhase_9 + DutyCycle - ignitionTime_tmp
        if sensorPhase_10 >= ignitionTime_tmp:
            time_10 = sensorPhase_10 - ignitionTime_tmp
        else:
            time_10 = sensorPhase_10 + DutyCycle - ignitionTime_tmp
        TotalSpotTime = TotalSpotTime + (
                time_1 + time_2 + time_3 + time_4 + time_5 + time_6 + time_7 + time_8 + time_9 + time_10) / 10
    Ave_SpotTimeMillisecond = ((float)(TotalSpotTime)) / 10
    Ave_SpotTime_Minute = round(Ave_SpotTimeMillisecond / 1000.0 / 60.0, 12)
    if Ave_SpotTime_Minute >= 0.000001:
        return Ave_SpotTime_Minute
    else:
        return 0.000001


def ResultOfSensorLifespan_Day(WakeupDuration, DeepsleepDuration):
    W = WakeupDuration
    D = DeepsleepDuration
    LifespanMillisecond = (float)(1.0 / ((((float)(W)) / 3600000.0) * WakeupEnergyCostPerHourPercentage + (((float)(
        D)) / 3600000.0) * DeepsleepEnergyCostPerHourPercentage + WakeupFromD0FunctionEnergyCostPerHourPercentage) * (
                                      (float)(W + D)))
    LifespanDay = round((LifespanMillisecond / 3600000.0 / 24.0), 12)
    return LifespanDay


def build_q_table(n_states, actions):
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))),  # q_table initial values
        columns=actions,  # actions's name
    )
    print(table)  # show table
    return table


def choose_action(state, q_table):
    # This is how to choose an action
    state_actions = q_table.iloc[state, :]

    if (np.random.uniform() > EPSILON) or ((state_actions == 0).all()):  # act non-greedy or state-action have no value
        action_name = np.random.choice(ACTIONS)
    else:  # act greedy
        action_name = state_actions.idxmax()  # replace argmax to idxmax as argmax means a different function in newer version of pandas
    return action_name


def MockActionToRealAction(A):
    if A == 'S2_phase_plus':
        sensorPhase_2_plus_Action()
    elif A == 'S3_phase_plus':
        sensorPhase_3_plus_Action()
    elif A == 'S4_phase_plus':
        sensorPhase_4_plus_Action()
    elif A == 'S5_phase_plus':
        sensorPhase_5_plus_Action()
    elif A == 'S6_phase_plus':
        sensorPhase_6_plus_Action()
    elif A == 'S7_phase_plus':
        sensorPhase_7_plus_Action()
    elif A == 'S8_phase_plus':
        sensorPhase_8_plus_Action()
    elif A == 'S9_phase_plus':
        sensorPhase_9_plus_Action()
    elif A == 'S10_phase_plus':
        sensorPhase_10_plus_Action()
    elif A == 'S2_phase_minus':
        sensorPhase_2_minus_Action()
    elif A == 'S3_phase_minus':
        sensorPhase_3_minus_Action()
    elif A == 'S4_phase_minus':
        sensorPhase_4_minus_Action()
    elif A == 'S5_phase_minus':
        sensorPhase_5_minus_Action()
    elif A == 'S6_phase_minus':
        sensorPhase_6_minus_Action()
    elif A == 'S7_phase_minus':
        sensorPhase_7_minus_Action()
    elif A == 'S8_phase_minus':
        sensorPhase_8_minus_Action()
    elif A == 'S9_phase_minus':
        sensorPhase_9_minus_Action()
    elif A == 'S10_phase_minus':
        sensorPhase_10_minus_Action()
    elif A == 'WakeupDuration_plus':
        WakeupDuration_plus_Action()
    elif A == 'WakeupDuration_minus':
        WakeupDuration_minus_Action()
    elif A == 'DeepsleepDuration_plus':
        DeepsleepDuration_plus_Action()
    elif A == 'DeepsleepDuration_minus':
        DeepsleepDuration_minus_Action()
    elif A == 'NoAction':
        pass
    else:
        pass


def ReverseBack(A):
    if A == 'S2_phase_plus':
        sensorPhase_2_minus_Action()
    elif A == 'S3_phase_plus':
        sensorPhase_3_minus_Action()
    elif A == 'S4_phase_plus':
        sensorPhase_4_minus_Action()
    elif A == 'S5_phase_plus':
        sensorPhase_5_minus_Action()
    elif A == 'S6_phase_plus':
        sensorPhase_6_minus_Action()
    elif A == 'S7_phase_plus':
        sensorPhase_7_minus_Action()
    elif A == 'S8_phase_plus':
        sensorPhase_8_minus_Action()
    elif A == 'S9_phase_plus':
        sensorPhase_9_minus_Action()
    elif A == 'S10_phase_plus':
        sensorPhase_10_minus_Action()
    elif A == 'S2_phase_minus':
        sensorPhase_2_plus_Action()
    elif A == 'S3_phase_minus':
        sensorPhase_3_plus_Action()
    elif A == 'S4_phase_minus':
        sensorPhase_4_plus_Action()
    elif A == 'S5_phase_minus':
        sensorPhase_5_plus_Action()
    elif A == 'S6_phase_minus':
        sensorPhase_6_plus_Action()
    elif A == 'S7_phase_minus':
        sensorPhase_7_plus_Action()
    elif A == 'S8_phase_minus':
        sensorPhase_8_plus_Action()
    elif A == 'S9_phase_minus':
        sensorPhase_9_plus_Action()
    elif A == 'S10_phase_minus':
        sensorPhase_10_plus_Action()
    elif A == 'WakeupDuration_plus':
        WakeupDuration_minus_Action()
    elif A == 'WakeupDuration_minus':
        WakeupDuration_plus_Action()
    elif A == 'DeepsleepDuration_plus':
        DeepsleepDuration_minus_Action()
    elif A == 'DeepsleepDuration_minus':
        DeepsleepDuration_plus_Action()
    elif A == 'NoAction':
        pass
    else:
        pass


def get_env_feedback(S, A):
    # This is how agent will interact with the environment
    R = 0.0
    Res1 = ResultOfSpotIgnition_Min(WakeupDuration, DeepsleepDuration, sensorPhase_2, sensorPhase_3, sensorPhase_4,
                                    sensorPhase_5, sensorPhase_6, sensorPhase_7, sensorPhase_8, sensorPhase_9,
                                    sensorPhase_10)
    Res2 = ResultOfSensorLifespan_Day(WakeupDuration, DeepsleepDuration)
    if A != 'NoAction' and A is not None:
        MockActionToRealAction(A)
        Res1_next = ResultOfSpotIgnition_Min(WakeupDuration, DeepsleepDuration, sensorPhase_2, sensorPhase_3,
                                             sensorPhase_4, sensorPhase_5, sensorPhase_6, sensorPhase_7, sensorPhase_8,
                                             sensorPhase_9, sensorPhase_10)
        Res2_next = ResultOfSensorLifespan_Day(WakeupDuration, DeepsleepDuration)
        ReverseBack(A)
        R = round((((Res1_next / Res1 - 1.0) / (0.01) * (RewardMarkOfSpotIgnitionTimeForEvery1Percent) + (
                Res2_next / Res2 - 1.0) / 0.01 * RewardMarkOfSensorLifespanForEvery1Percent) + RewardMarkOfActionPenalty),
                  12)
    elif A == 'NoAction':
        R = round(RewardMarkOfSensorLifespanForEvery1Percent, 8)
    if S == trainingStepPerEpisode:
        S_ = trainingStepPerEpisode
    else:
        S_ = S + 1
    return S_, R


def update_env_1(S, episode, step_counter):
    # This is how environment be updated
    if S == trainingStepPerEpisode:
        try:
            Res1_now = ResultOfSpotIgnition_Min(WakeupDuration, DeepsleepDuration, sensorPhase_2, sensorPhase_3,
                                                sensorPhase_4, sensorPhase_5, sensorPhase_6, sensorPhase_7,
                                                sensorPhase_8, sensorPhase_9, sensorPhase_10)
            Res2_now = ResultOfSensorLifespan_Day(WakeupDuration, DeepsleepDuration)
            Res1_0 = ResultOfSpotIgnition_Min(WakeupDuration_0, DeepsleepDuration_0, sensorPhase_2_0, sensorPhase_3_0,
                                              sensorPhase_4_0, sensorPhase_5_0, sensorPhase_6_0, sensorPhase_7_0,
                                              sensorPhase_8_0, sensorPhase_9_0, sensorPhase_10_0)
            Res2_0 = ResultOfSensorLifespan_Day(WakeupDuration_0, DeepsleepDuration_0)
        except:
            Reward_total = RewardMarkOfSensorLifespanForEvery1Percent
        else:
            Reward_total = round((((Res1_now / Res1_0 - 1.0) / (0.01) * (
                RewardMarkOfSpotIgnitionTimeForEvery1Percent) + (
                                           Res2_now / Res2_0 - 1.0) / 0.01 * RewardMarkOfSensorLifespanForEvery1Percent) + RewardMarkOfActionPenalty),
                                 12)
        '''interaction = 'Episode %s: total_steps = %s \n' % (episode + 1, step_counter) print( '\nReward_total gonna 
        be %.12f. Result shall be ended like %.12f and %.12f for the sensor\'s phase of:\n 2: %d; 3: %d; 4: %d; 5: 
        %d; 6: %d; 7: %d; 8: %d;  9: %d; 10: %d' % ( (Reward_total), ResultOfSensorLifespan_Day(WakeupDuration, 
        DeepsleepDuration), ResultOfSpotIgnition_Min(WakeupDuration, DeepsleepDuration, sensorPhase_2, sensorPhase_3, 
        sensorPhase_4, sensorPhase_5, sensorPhase_6, sensorPhase_7, sensorPhase_8, sensorPhase_9, sensorPhase_10), 
        ResultOfSensorLifespan_Day(WakeupDuration, DeepsleepDuration), sensorPhase_2, sensorPhase_3, sensorPhase_4, 
        sensorPhase_5, sensorPhase_6, sensorPhase_7, sensorPhase_8, sensorPhase_9, sensorPhase_10)) print('\r{
        }'.format(interaction), end='') '''
        time.sleep(2)
        print('\r                                ', end='')
    else:
        '''
        interaction = 'The Changing Trend result goes like %.12f. Result shall be ended like %.12f and %.12f for the sensor\'s phase of:\n 2: %d; 3: %d; 4: %d; 5: %d; 6: %d; 7: %d; 8: %d;  9: %d; 10: %d' % (
        (Reward_total), ResultOfSensorLifespan_Day(WakeupDuration, DeepsleepDuration),ResultOfSpotIgnition_Min(WakeupDuration, DeepsleepDuration, sensorPhase_2,sensorPhase_3,sensorPhase_4,sensorPhase_5,sensorPhase_6,sensorPhase_7,sensorPhase_8,sensorPhase_9,sensorPhase_10), ResultOfSensorLifespan_Day(WakeupDuration, DeepsleepDuration), sensorPhase_2, sensorPhase_3, sensorPhase_4, sensorPhase_5, sensorPhase_6, sensorPhase_7 ,sensorPhase_8, sensorPhase_9, sensorPhase_10)
        print('\r{}'.format(interaction), 'step:', step_counter, end='')
        '''
        time.sleep(FRESH_TIME)
    if S == trainingStepPerEpisode:
        S = trainingStepPerEpisode
    return S


def update_env_2(S, episode, step_counter):
    # This is how environment be updated
    if S == (trainingStepPerEpisode + 1):
        try:
            Res1_now = ResultOfSpotIgnition_Min(WakeupDuration, DeepsleepDuration, sensorPhase_2, sensorPhase_3,
                                                sensorPhase_4, sensorPhase_5, sensorPhase_6, sensorPhase_7,
                                                sensorPhase_8, sensorPhase_9, sensorPhase_10)
            Res2_now = ResultOfSensorLifespan_Day(WakeupDuration, DeepsleepDuration)
            Res1_0 = ResultOfSpotIgnition_Min(WakeupDuration_0, DeepsleepDuration_0, sensorPhase_2_0, sensorPhase_3_0,
                                              sensorPhase_4_0, sensorPhase_5_0, sensorPhase_6_0, sensorPhase_7_0,
                                              sensorPhase_8_0, sensorPhase_9_0, sensorPhase_10_0)
            Res2_0 = ResultOfSensorLifespan_Day(WakeupDuration_0, DeepsleepDuration_0)
        except:
            Reward_total = RewardMarkOfSensorLifespanForEvery1Percent
        else:
            Reward_total = round((((Res1_now / Res1_0 - 1.0) / (0.01) * (
                RewardMarkOfSpotIgnitionTimeForEvery1Percent) + (
                                           Res2_now / Res2_0 - 1.0) / 0.01 * RewardMarkOfSensorLifespanForEvery1Percent) + RewardMarkOfActionPenalty),
                                 12)

        interaction = 'Episode %s: total_steps = %s \n' % (episode + 1, step_counter - 1)
        print(
            '\nReward_total gonna be %.12f. Result shall be ended like Lifespan: %.12f Day and Spot Speed: %.12f min '
            '\nWakeup Duration = %d millisecond; Deepsleep Duration = %d millisecond;\nfor the sensor\'s phase of: 2: '
            '%d; 3: %d; 4: %d; 5: %d; 6: %d; 7: %d; 8: %d;  9: %d; 10: %d' % (
                Reward_total, ResultOfSensorLifespan_Day(WakeupDuration, DeepsleepDuration),
                ResultOfSpotIgnition_Min(WakeupDuration, DeepsleepDuration, sensorPhase_2, sensorPhase_3, sensorPhase_4,
                                         sensorPhase_5, sensorPhase_6, sensorPhase_7, sensorPhase_8, sensorPhase_9,
                                         sensorPhase_10), WakeupDuration, DeepsleepDuration, sensorPhase_2,
                sensorPhase_3,
                sensorPhase_4, sensorPhase_5, sensorPhase_6, sensorPhase_7, sensorPhase_8, sensorPhase_9,
                sensorPhase_10))
        print('\r{}'.format(interaction), end='')
        time.sleep(FRESH_TIME)
        print('\r                                ', end='')
    else:
        if step_counter - 1 == trainingStepPerEpisode + 1:
            if episode == MAX_EPISODES - 1:
                tmp_step = trainingStepPerEpisode
            else:
                tmp_step = 0
            interaction_1 = 'Step %d - The Changing Trend result goes like Lifespan: %.12f Day and Spot Speed: %.12f ' \
                            'min； ' % (
                tmp_step, ResultOfSensorLifespan_Day(WakeupDuration, DeepsleepDuration),
                ResultOfSpotIgnition_Min(WakeupDuration, DeepsleepDuration, sensorPhase_2, sensorPhase_3, sensorPhase_4,
                                         sensorPhase_5, sensorPhase_6, sensorPhase_7, sensorPhase_8, sensorPhase_9,
                                         sensorPhase_10))
        else:
            interaction_1 = 'Step %d - The Changing Trend result goes like Lifespan: %.12f Day and Spot Speed: %.12f ' \
                            'min； ' % (
                step_counter, ResultOfSensorLifespan_Day(WakeupDuration, DeepsleepDuration),
                ResultOfSpotIgnition_Min(WakeupDuration, DeepsleepDuration, sensorPhase_2, sensorPhase_3, sensorPhase_4,
                                         sensorPhase_5, sensorPhase_6, sensorPhase_7, sensorPhase_8, sensorPhase_9,
                                         sensorPhase_10))
        interaction_2 = 'Wakeup Duration = %d millisecond; Deepsleep Duration = %d millisecond;' % (
            WakeupDuration, DeepsleepDuration)
        # interaction_3 = '''for the sensor\'s phase of: 2: %d; 3: %d; 4: %d; 5: %d; 6: %d; 7: %d; 8: %d;  9: %d; 10:
        # %d '''% (sensorPhase_2, sensorPhase_3, sensorPhase_4, sensorPhase_5, sensorPhase_6, sensorPhase_7 ,
        # sensorPhase_8, sensorPhase_9, sensorPhase_10)
        interaction_3 = ''
        # print('\r{}'.format(interaction_1), end='')
        # print('\r{}'.format(interaction_2), end='')
        print('\r{}'.format(interaction_1 + interaction_2 + interaction_3), end='')
        time.sleep(FRESH_TIME)
    if S == trainingStepPerEpisode:
        S = trainingStepPerEpisode
    return S


def FinalReport():
    Res1_0 = ResultOfSpotIgnition_Min(WakeupDuration_0, DeepsleepDuration_0, sensorPhase_2_0, sensorPhase_3_0,
                                      sensorPhase_4_0, sensorPhase_5_0, sensorPhase_6_0, sensorPhase_7_0,
                                      sensorPhase_8_0, sensorPhase_9_0, sensorPhase_10_0)
    Res2_0 = ResultOfSensorLifespan_Day(WakeupDuration_0, DeepsleepDuration_0)
    print('\nTraining from ', Res2_0, ' Days and ', Res1_0, ' min;\n', 'WakeupDuration = ', WakeupDuration_0,
          '; DeepsleepDuration = ', DeepsleepDuration_0, ';\n sensorPhase_2 = ', sensorPhase_2_0, '; sensorPhase_3 = ',
          sensorPhase_3_0, '; sensorPhase_4 = ', sensorPhase_4_0, '; sensorPhase_5 = ', sensorPhase_5_0,
          ';\n sensorPhase_6 = ', sensorPhase_6_0, '; sensorPhase_7 = ', sensorPhase_7_0, '; sensorPhase_8 = ',
          sensorPhase_8_0, '; sensorPhase_9 = ', sensorPhase_9_0, '; sensorPhase_10 = ', sensorPhase_10_0)
    print(
        '\nResult shall be ended like - Lifespan: %.12f Day and Spot Speed: %.12f min \nWakeup Duration = %d '
        'millisecond; Deepsleep Duration = %d millisecond;\nfor the sensor\'s phase of: 2: %d; 3: %d; 4: %d; 5: %d; '
        '6: %d; 7: %d; 8: %d;  9: %d; 10: %d' % (
            ResultOfSensorLifespan_Day(WakeupDuration, DeepsleepDuration),
            ResultOfSpotIgnition_Min(WakeupDuration, DeepsleepDuration, sensorPhase_2, sensorPhase_3, sensorPhase_4,
                                     sensorPhase_5, sensorPhase_6, sensorPhase_7, sensorPhase_8, sensorPhase_9,
                                     sensorPhase_10), WakeupDuration, DeepsleepDuration, sensorPhase_2, sensorPhase_3,
            sensorPhase_4, sensorPhase_5, sensorPhase_6, sensorPhase_7, sensorPhase_8, sensorPhase_9, sensorPhase_10))

    try:
        Res1_now = ResultOfSpotIgnition_Min(WakeupDuration, DeepsleepDuration, sensorPhase_2, sensorPhase_3,
                                            sensorPhase_4, sensorPhase_5, sensorPhase_6, sensorPhase_7, sensorPhase_8,
                                            sensorPhase_9, sensorPhase_10)
        Res2_now = ResultOfSensorLifespan_Day(WakeupDuration, DeepsleepDuration)
        Res1_0 = ResultOfSpotIgnition_Min(WakeupDuration_0, DeepsleepDuration_0, sensorPhase_2_0, sensorPhase_3_0,
                                          sensorPhase_4_0, sensorPhase_5_0, sensorPhase_6_0, sensorPhase_7_0,
                                          sensorPhase_8_0, sensorPhase_9_0, sensorPhase_10_0)
        Res2_0 = ResultOfSensorLifespan_Day(WakeupDuration_0, DeepsleepDuration_0)
    except:
        Reward_total = RewardMarkOfSensorLifespanForEvery1Percent
    else:
        Reward_total = round((((Res1_now / Res1_0 - 1.0) / (0.01) * (RewardMarkOfSpotIgnitionTimeForEvery1Percent) + (
                Res2_now / Res2_0 - 1.0) / 0.01 * RewardMarkOfSensorLifespanForEvery1Percent) + RewardMarkOfActionPenalty),
                             12)
    print("\nReward_total gonna be %.12f" % Reward_total)


def findMinAbs(array):
    if array == None or len(array) <= 0:
        print("Fail to find Min Abs! Gonna return 0!")
        return 0
    mins = 2 ** 32
    i = 0
    while i < len(array):
        if abs(array[i]) < abs(mins) and abs(array[i]) != 1.0:
            mins = abs(array[i])
        i += 1
    return mins


def RL():
    # main part of RL loop

    q_table = build_q_table(N_STATES, ACTIONS)
    for episode in range(MAX_EPISODES):
        resetGlobalParametersBackToDefaultValue()
        step_counter = 0
        S = 0
        List_for_stop_judger = []
        is_terminated = False
        S = update_env_1(S, episode, step_counter)
        while not is_terminated:
            A = choose_action(S, q_table)
            S_, R = get_env_feedback(S, A)  # take action & get next state and reward
            q_predict = q_table.loc[S, A]
            if S != trainingStepPerEpisode + 1:
                q_target = R + GAMMA * q_table.iloc[S_, :].max()  # next state is not terminal
            else:
                q_target = R  # next state is terminal
                is_terminated = True  # terminate this episode
            q_table.loc[S, A] += ALPHA * (q_target - q_predict)  # update

            Res1 = ResultOfSpotIgnition_Min(WakeupDuration, DeepsleepDuration, sensorPhase_2, sensorPhase_3,
                                            sensorPhase_4, sensorPhase_5, sensorPhase_6, sensorPhase_7, sensorPhase_8,
                                            sensorPhase_9, sensorPhase_10)
            Res2 = ResultOfSensorLifespan_Day(WakeupDuration, DeepsleepDuration)
            MockActionToRealAction(A)
            Res1_next = ResultOfSpotIgnition_Min(WakeupDuration, DeepsleepDuration, sensorPhase_2, sensorPhase_3,
                                                 sensorPhase_4, sensorPhase_5, sensorPhase_6, sensorPhase_7,
                                                 sensorPhase_8, sensorPhase_9, sensorPhase_10)
            Res2_next = ResultOfSensorLifespan_Day(WakeupDuration, DeepsleepDuration)
            Reward_now = round((((Res1_next / Res1 - 1.0) / 0.01 * RewardMarkOfSpotIgnitionTimeForEvery1Percent + (
                    Res2_next / Res2 - 1.0) / 0.01 * RewardMarkOfSensorLifespanForEvery1Percent) + RewardMarkOfActionPenalty),
                               12)

            List_for_stop_judger.append(Reward_now)
            if len(List_for_stop_judger) >= 16:
                StopJudgerBasedOnReward = (findMinAbs(List_for_stop_judger[15:25]) / 5.0 + 0.0)
                if (abs(List_for_stop_judger[-1]) < StopJudgerBasedOnReward and abs(List_for_stop_judger[-1]) != abs(
                        RewardMarkOfActionPenalty)) or S == trainingStepPerEpisode:
                    S_ = trainingStepPerEpisode + 1

            S = S_  # move to next state

            S = update_env_2(S, episode, step_counter + 1)
            step_counter += 1

    return q_table


if __name__ == "__main__":
    print("Start Q-training; please wait ......\n...\n...\n")

    now = datetime.now()
    DataFileName_time = now.strftime('%Y-%m-%d_%H-%M-%S')
    StepNum = '_~_%s' % trainingStepPerEpisode + '_step'
    EpisodeNum = '%s' % MAX_EPISODES + '_episode'
    Txt = ".txt"
    FileName = DataFileName_time + StepNum + '_x_' + EpisodeNum + Txt
    path = 'TrainingData/' + FileName

    original_stdout = sys.stdout  # Save a reference to the original standard output
    sys.stdout = open(path, 'w+')

    q_table = RL()
    print('\r\n\nQ-table:')
    print('', q_table)
    FinalReport()

    sys.stdout.close()
    sys.stdout = original_stdout

    print("\n\nEnd Q-training!\n")
    FinalReport()

    EndProgram = input('')
    sys.exit()
