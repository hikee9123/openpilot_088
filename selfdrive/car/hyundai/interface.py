#!/usr/bin/env python3
from cereal import car
from selfdrive.config import Conversions as CV
from selfdrive.car.hyundai.values import CAR, EV_CAR, HYBRID_CAR
from selfdrive.car import STD_CARGO_KG, scale_rot_inertia, scale_tire_stiffness, gen_empty_fingerprint
from selfdrive.car.interfaces import CarInterfaceBase

from common.params import Params
class CarInterface(CarInterfaceBase):

  @staticmethod
  def compute_gb(accel, speed):
    return float(accel) / 3.0

  @staticmethod
  def get_params(candidate, fingerprint=gen_empty_fingerprint(), car_fw=[]):  # pylint: disable=dangerous-default-value
    ret = CarInterfaceBase.get_std_params(candidate, fingerprint)

    ret.carName = "hyundai"
    ret.safetyModel = car.CarParams.SafetyModel.hyundai
    ret.radarOffCan = False

    # Most Hyundai car ports are community features for now
    ret.communityFeature = candidate not in [CAR.SONATA, CAR.PALISADE]

    ret.steerActuatorDelay = 0.1  # Default delay
    ret.steerRateCost = 0.5
    ret.steerLimitTimer = 0.4
    tire_stiffness_factor = 1.

    ret.startAccel = 1.0

    if candidate == CAR.GRANDEUR_HEV_19:
      ret.mass = 1675. + STD_CARGO_KG
      ret.wheelbase = 2.845
      ret.steerRatio = 16.5  #13.96   #12.5
      ret.steerMaxBP = [0.]
      ret.steerMaxV = [1.0]
      ret.steerRateCost = 1.2
      ret.minSteerSpeed = 1 * CV.KPH_TO_MS

      ret.lateralTuning.pid.kf = 0.000005
      ret.lateralTuning.pid.kpBP, ret.lateralTuning.pid.kpV = [[0.], [0.15]]
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kiV = [[0.], [0.01]]

      
      ret.lateralTuning.init('lqr')
      ret.lateralTuning.lqr.scale = 1700     #1700.0
      ret.lateralTuning.lqr.ki = 0.01       #0.01
      ret.lateralTuning.lqr.dcGain = 0.00289  #0.00285   # 0.002237852961363602
      # 호야  1500, 0.015, 0.0027
      #  1700, 0.01, 0.0029
      #  2000, 0.01, 0.003
      ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
      ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
      ret.lateralTuning.lqr.c = [1., 0.]
      ret.lateralTuning.lqr.k = [-110., 451.]
      ret.lateralTuning.lqr.l = [0.33, 0.318]
      """
      ret.lateralTuning.init('indi')
      ret.lateralTuning.indi.innerLoopGainBP = [0.]
      ret.lateralTuning.indi.innerLoopGainV = [3.5]
      ret.lateralTuning.indi.outerLoopGainBP = [0.]
      ret.lateralTuning.indi.outerLoopGainV = [2.0]
      ret.lateralTuning.indi.timeConstantBP = [0.]
      ret.lateralTuning.indi.timeConstantV = [1.4]               # 2. 중앙 조정
      ret.lateralTuning.indi.actuatorEffectivenessBP = [0.]
      ret.lateralTuning.indi.actuatorEffectivenessV = [5.3]      # 1. 낮을수록 코너를 잘돔.  (직진 와리 가리 조정)
      """
    elif candidate == CAR.SANTA_FE:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 3982. * CV.LB_TO_KG + STD_CARGO_KG
      ret.wheelbase = 2.766
      # Values from optimizer
      ret.steerRatio = 16.55  # 13.8 is spec end-to-end
      tire_stiffness_factor = 0.82
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[9., 22.], [9., 22.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.2, 0.35], [0.05, 0.09]]
    elif candidate in [CAR.SONATA, CAR.SONATA_HYBRID]:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 1513. + STD_CARGO_KG
      ret.wheelbase = 2.84
      ret.steerRatio = 13.27 * 1.15   # 15% higher at the center seems reasonable
      tire_stiffness_factor = 0.65
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate == CAR.SONATA_LF:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 4497. * CV.LB_TO_KG
      ret.wheelbase = 2.804
      ret.steerRatio = 13.27 * 1.15   # 15% higher at the center seems reasonable
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate == CAR.PALISADE:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 1999. + STD_CARGO_KG
      ret.wheelbase = 2.90
      ret.steerRatio = 15.6 * 1.15
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.3], [0.05]]
    elif candidate in [CAR.ELANTRA, CAR.ELANTRA_GT_I30]:
      ret.lateralTuning.pid.kf = 0.00006
      ret.mass = 1275. + STD_CARGO_KG
      ret.wheelbase = 2.7
      ret.steerRatio = 15.4            # 14 is Stock | Settled Params Learner values are steerRatio: 15.401566348670535
      tire_stiffness_factor = 0.385    # stiffnessFactor settled on 1.0081302973865127
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      ret.minSteerSpeed = 32 * CV.MPH_TO_MS
    elif candidate == CAR.ELANTRA_2021:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = (2800. * CV.LB_TO_KG) + STD_CARGO_KG
      ret.wheelbase = 2.72
      ret.steerRatio = 12.9
      tire_stiffness_factor = 0.65
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate == CAR.ELANTRA_HEV_2021:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = (3017. * CV.LB_TO_KG) + STD_CARGO_KG
      ret.wheelbase = 2.72
      ret.steerRatio = 12.9
      tire_stiffness_factor = 0.65
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate == CAR.HYUNDAI_GENESIS:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 2060. + STD_CARGO_KG
      ret.wheelbase = 3.01
      ret.steerRatio = 16.5
      ret.lateralTuning.init('indi')
      ret.lateralTuning.indi.innerLoopGainBP = [0.]
      ret.lateralTuning.indi.innerLoopGainV = [3.5]
      ret.lateralTuning.indi.outerLoopGainBP = [0.]
      ret.lateralTuning.indi.outerLoopGainV = [2.0]
      ret.lateralTuning.indi.timeConstantBP = [0.]
      ret.lateralTuning.indi.timeConstantV = [1.4]
      ret.lateralTuning.indi.actuatorEffectivenessBP = [0.]
      ret.lateralTuning.indi.actuatorEffectivenessV = [2.3]
      ret.minSteerSpeed = 60 * CV.KPH_TO_MS
    elif candidate in [CAR.KONA, CAR.KONA_EV, CAR.KONA_HEV]:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = {CAR.KONA_EV: 1685., CAR.KONA_HEV: 1425.}.get(candidate, 1275.) + STD_CARGO_KG
      ret.wheelbase = 2.7
      ret.steerRatio = 13.73 * 1.15  # Spec
      tire_stiffness_factor = 0.385
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate in [CAR.IONIQ, CAR.IONIQ_EV_LTD, CAR.IONIQ_EV_2020, CAR.IONIQ_PHEV]:
      ret.lateralTuning.pid.kf = 0.00006
      ret.mass = 1490. + STD_CARGO_KG  # weight per hyundai site https://www.hyundaiusa.com/ioniq-electric/specifications.aspx
      ret.wheelbase = 2.7
      ret.steerRatio = 13.73  # Spec
      tire_stiffness_factor = 0.385
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      if candidate not in [CAR.IONIQ_EV_2020, CAR.IONIQ_PHEV]:
        ret.minSteerSpeed = 32 * CV.MPH_TO_MS
    elif candidate == CAR.VELOSTER:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 3558. * CV.LB_TO_KG
      ret.wheelbase = 2.80
      ret.steerRatio = 13.75 * 1.15
      tire_stiffness_factor = 0.5
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]

    # Kia
    elif candidate == CAR.KIA_SORENTO:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 1985. + STD_CARGO_KG
      ret.wheelbase = 2.78
      ret.steerRatio = 14.4 * 1.1   # 10% higher at the center seems reasonable
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate in [CAR.KIA_NIRO_EV, CAR.KIA_NIRO_HEV, CAR.KIA_NIRO_HEV_2021]:
      ret.lateralTuning.pid.kf = 0.00006
      ret.mass = 1737. + STD_CARGO_KG
      ret.wheelbase = 2.7
      ret.steerRatio = 13.9 if CAR.KIA_NIRO_HEV_2021 else 13.73  # Spec
      tire_stiffness_factor = 0.385
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      if candidate == CAR.KIA_NIRO_HEV:
        ret.minSteerSpeed = 32 * CV.MPH_TO_MS
    elif candidate == CAR.KIA_SELTOS:
      ret.mass = 1337. + STD_CARGO_KG
      ret.wheelbase = 2.63
      ret.steerRatio = 14.56
      tire_stiffness_factor = 1
      ret.lateralTuning.init('indi')
      ret.lateralTuning.indi.innerLoopGainBP = [0.]
      ret.lateralTuning.indi.innerLoopGainV = [4.]
      ret.lateralTuning.indi.outerLoopGainBP = [0.]
      ret.lateralTuning.indi.outerLoopGainV = [3.]
      ret.lateralTuning.indi.timeConstantBP = [0.]
      ret.lateralTuning.indi.timeConstantV = [1.4]
      ret.lateralTuning.indi.actuatorEffectivenessBP = [0.]
      ret.lateralTuning.indi.actuatorEffectivenessV = [1.8]
    elif candidate in [CAR.KIA_OPTIMA, CAR.KIA_OPTIMA_H]:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 3558. * CV.LB_TO_KG
      ret.wheelbase = 2.80
      ret.steerRatio = 13.75
      tire_stiffness_factor = 0.5
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate == CAR.KIA_STINGER:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 1825. + STD_CARGO_KG
      ret.wheelbase = 2.78
      ret.steerRatio = 14.4 * 1.15   # 15% higher at the center seems reasonable
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate == CAR.KIA_FORTE:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 3558. * CV.LB_TO_KG
      ret.wheelbase = 2.80
      ret.steerRatio = 13.75
      tire_stiffness_factor = 0.5
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate == CAR.KIA_CEED:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 1450. + STD_CARGO_KG
      ret.wheelbase = 2.65
      ret.steerRatio = 13.75
      tire_stiffness_factor = 0.5
      ret.lateralTuning.pid.kf = 0.00005
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]

    # Genesis
    elif candidate == CAR.GENESIS_G70:
      ret.lateralTuning.init('indi')
      ret.lateralTuning.indi.innerLoopGainBP = [0.]
      ret.lateralTuning.indi.innerLoopGainV = [2.5]
      ret.lateralTuning.indi.outerLoopGainBP = [0.]
      ret.lateralTuning.indi.outerLoopGainV = [3.5]
      ret.lateralTuning.indi.timeConstantBP = [0.]
      ret.lateralTuning.indi.timeConstantV = [1.4]
      ret.lateralTuning.indi.actuatorEffectivenessBP = [0.]
      ret.lateralTuning.indi.actuatorEffectivenessV = [1.8]
      ret.steerActuatorDelay = 0.1
      ret.mass = 1640.0 + STD_CARGO_KG
      ret.wheelbase = 2.84
      ret.steerRatio = 13.56
    elif candidate == CAR.GENESIS_G80:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 2060. + STD_CARGO_KG
      ret.wheelbase = 3.01
      ret.steerRatio = 16.5
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.16], [0.01]]
    elif candidate == CAR.GENESIS_G90:
      ret.mass = 2200
      ret.wheelbase = 3.15
      ret.steerRatio = 12.069
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.16], [0.01]]

    # these cars require a special panda safety mode due to missing counters and checksums in the messages
    if candidate in [CAR.HYUNDAI_GENESIS, CAR.IONIQ_EV_2020, CAR.IONIQ_EV_LTD, CAR.IONIQ_PHEV, CAR.IONIQ, CAR.KONA_EV, CAR.KIA_SORENTO,
                     CAR.SONATA_LF, CAR.KIA_NIRO_EV, CAR.KIA_OPTIMA, CAR.VELOSTER, CAR.KIA_STINGER, CAR.KIA_SELTOS,
                     CAR.GENESIS_G70, CAR.GENESIS_G80, CAR.KIA_CEED, CAR.ELANTRA,
                     CAR.GRANDEUR_HEV_19]:
      ret.safetyModel = car.CarParams.SafetyModel.hyundaiLegacy

      ret.safetyModel = car.CarParams.SafetyModel.hyundaiCommunity
    
    # set appropriate safety param for gas signal
    if candidate in HYBRID_CAR:
      ret.safetyParam = 2
    elif candidate in EV_CAR:
      ret.safetyParam = 1

    ret.centerToFront = ret.wheelbase * 0.4

    # TODO: get actual value, for now starting with reasonable value for
    # civic and scaling by mass and wheelbase
    ret.rotationalInertia = scale_rot_inertia(ret.mass, ret.wheelbase)
    ret.openpilotLongitudinalControl = Params().get('LongitudinalControl') == b'1'  #False

    # TODO: start from empirically derived lateral slip stiffness for the civic and scale by
    # mass and CG position, so all cars will have approximately similar dyn behaviors
    ret.tireStiffnessFront, ret.tireStiffnessRear = scale_tire_stiffness(ret.mass, ret.wheelbase, ret.centerToFront,
                                                                         tire_stiffness_factor=tire_stiffness_factor)

    ret.enableBsm = 0x58b in fingerprint[0]

    return ret

  def update(self, c, can_strings):
    self.cp.update_strings(can_strings)
    self.cp_cam.update_strings(can_strings)

    ret = self.CS.update(self.cp, self.cp_cam)
    ret.canValid = self.cp.can_valid and self.cp_cam.can_valid
    ret.steeringRateLimited = self.CC.steer_rate_limited if self.CC is not None else False

    events = self.create_common_events(ret)

    # low speed steer alert hysteresis logic (only for cars with steer cut off above 10 m/s)
    if ret.vEgo < (self.CP.minSteerSpeed + 2.) and self.CP.minSteerSpeed > 10.:
      self.low_speed_alert = True
    if ret.vEgo > (self.CP.minSteerSpeed + 4.):
      self.low_speed_alert = False
    if self.low_speed_alert:
      events.add(car.CarEvent.EventName.belowSteerSpeed)
    elif self.CS.lkas_button_on == 15:
      events.add(car.CarEvent.EventName.invalidLkasSetting)
    

    ret.events = events.to_msg()

    self.CS.out = ret.as_reader()
    return self.CS.out

  def apply(self, c):
    can_sends = self.CC.update( c, self.CS, self.frame )

    self.frame += 1
    return can_sends
