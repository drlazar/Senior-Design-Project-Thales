import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.special as sp

## POWER
# pwr_recv
# pwr_trans
# power_flux_density
# isotropic_radiator_power_flux_density
# EIRP

## GAINS
# n_rad/antenna efficiency
# directivity
# gain_trans
# gain_recv

## LOSSES
# FSL - free space loss
# RSL - received feeder loss
# AML - antenna misalignment loss
# AA - atmospheric absorption
# PL - polarization mismatch loss
# K - boltzmann constant
# Total_Loss - sum of all above losses

## RATIOS
# SNR - signal to noise ratio
# CNR - carrier to noise ratio
# Eb_No - information bit ratio (derived from CNR, with transmission rate instead)
# Es_No - channel symbols ratio (meaning spectral efficiency energy to noise ratio, and derived from CNR, with trans_rate/bandwidth)

class Calculate:

    def __init__(self):
        self.modulation_dict = {'QPSK': 2,'8PSK': 3,'16APSK': 4,'32APSK': 5,'64APSK': 6}
        
    def mod_scheme(self, mod_type):
        return self.modulation_dict[mod_type]
    
    
    def power_flux_density(self, pwr_sup, sphere_rad):
        area = 4 * np.pi * (sphere_rad**2)
        pfd = pwr_sup / area #watts per meter squared
        return pfd

    def effective_isotropic_radiated_power_db(self, pwr_trans_db, gain_trans_db):
        eirp = pwr_trans_db + gain_trans_db
        return eirp
    
    def power_received_db(self, eirp, gain_recv_db):
        power_recv = eirp + gain_recv_db
        return power_recv
    
    def convert_to_decibel(self, value):
        decibels = 10 * np.log10(value)
        return decibels
    
    def decibel_to_std(self, value):
        div = value / 10
        std = 10**div
        return std
    
    def gain(self, aperture_efficiency, aperture_area, wavelength):
        num = 4 * np.pi * aperture_efficiency * aperture_area
        denom = np.power(wavelength, 2)
        ig = num / denom
        return ig
    
    def power_received(self, eirp, gain_received, losses):
        return eirp + gain_received - losses

    def carrier_noise_ratio(self, power_recv, T_sys, total_loss_db, bandwidth):
        boltzmann = 1.38064852 * (10**-23)
        boltzmann_db = self.convert_to_decibel(boltzmann)
        bandwidth_db = self.convert_to_decibel(bandwidth)
        gains = power_recv
        losses = self.convert_to_decibel(T_sys) + boltzmann_db + total_loss_db + bandwidth_db
        cnr = gains - losses
        return cnr
    
    def free_space_path_loss(self, dist_trav_km, bandwidth_freq): #fsl
        num = 4 * np.pi * dist_trav_km * 1000 * bandwidth_freq
        denom = 2.99792458 * 10**8
        fspl = np.power(num / denom, 2)
        return fspl
    
    def total_loss(self, fsl, rfl, aml, aa, pl):
        return fsl + rfl + aml + aa + pl
    
    def data_rate(self, bandwidth, cnr):
        return bandwidth*np.log2(1 + self.decibel_to_std(cnr))
    
    def ip_rate_mbps(self, overhead, bandwidth_MHz, multiplier, code_rate, roll_off):
        info_rate = overhead * bandwidth_MHz * multiplier * (code_rate / roll_off)
        return info_rate

    def ebno(self, cnr, bandwidth, data_rate):
        eb_no = cnr + self.convert_to_decibel(bandwidth) - self.convert_to_decibel(data_rate)
        return eb_no
    
    def esno(self,  ebno, M):
        es_no = self.convert_to_decibel(self.decibel_to_std(ebno)*M)
        return es_no
    
    def symbol_rate(self, data_rate, M, code_rate):
        return data_rate / (M * code_rate)
        
    
    def link_margin(self, ebno, ebno_req):
        error = ebno - ebno_req
        return error
    
    def MPSK_error(self, M, EbNo):
        return sp.erfc(np.sqrt(self.decibel_to_std(EbNo) * np.log2(M)) * np.sin(np.pi/M)) / np.log2(M)
    
    def display_BER(self):
        EbNo = np.array(range(37))
        plt.plot(EbNo, self.MPSK_error(2, EbNo), label="BPSK")
        plt.plot(EbNo, self.MPSK_error(4, EbNo), label="QPSK")
        plt.plot(EbNo, self.MPSK_error(8, EbNo), label="8PSK")
        plt.plot(EbNo, self.MPSK_error(16, EbNo), label="16PSK")
        plt.plot(EbNo, self.MPSK_error(32, EbNo), label="32PSK")
        plt.plot(EbNo, self.MPSK_error(64, EbNo), label="64PSK")
        plt.title("Bit Error Rate vs EbNo")
        plt.xlabel("Eb/No (dB)")
        plt.ylabel("BER")
        plt.yscale("log")
        plt.ylim(10**-19, 1)
        plt.legend()
        plt.show()
        
    def calc_link_budget(self, bandwidth, distance_km, pwr_trans_dbW, gain_trans_dbi, gain_recv_dbi, Tsys, MPSK, code_rate, overhead, rolloff):
        bandwidth_db = self.convert_to_decibel(bandwidth)
        fsl = calc.convert_to_decibel(calc.free_space_path_loss(distance_km, bandwidth))
        total_loss = fsl+5
        eirp = calc.effective_isotropic_radiated_power_db(pwr_trans_dbW, gain_trans_dbi)
        pwr_recv = calc.power_received_db(eirp, gain_recv_dbi)
        cnr = calc.carrier_noise_ratio(pwr_recv, Tsys, total_loss, bandwidth)
        data_rate = calc.data_rate(bandwidth, cnr)    
        ebno = calc.ebno(cnr, bandwidth, data_rate)      
        M = np.log2(MPSK)
        esno = calc.esno(ebno, M)
        spectral_eff = calc.ip_rate_mbps(overhead,  bandwidth, M, code_rate, rolloff) / bandwidth      
        calc.display_BER()
        
        params = {"Bandwidth (dBHz)": bandwidth_db, 
             "Free Space Loss (dB)": fsl, 
             "Total Loss (dB)": total_loss, 
             "Power Transmitted (dBW)": pwr_trans_dbW,
             "Gain Transmitted (dBi)": gain_trans_dbi,
             "Gain Received (dBi)": gain_recv_dbi,
             "Power Received (dBW)": pwr_recv,
             "C/N (dB)": cnr,
             "Data Rate": data_rate,
             "Modulation": MPSK,
             "Eb/No (dB)": ebno,
             "Es/No (dB)": esno,
             "Spectral Efficiency": spectral_eff}
        lb = pd.DataFrame(data=params)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', None)
        print(lb)
        return lb
        

## FUNCTION DEBUG ##
calc = Calculate()
bandwidth = 315 * 10**6
distance_km = np.array([35786])
pwr_trans_db = 10
gain_trans_db = -15
gain_recv_db = -15
Tsys = 300
MPSK = 32
code_rate = 0.86
overhead = 1
rolloff = 1
calc.calc_link_budget(bandwidth, distance_km, pwr_trans_db, gain_trans_db, gain_recv_db, Tsys, MPSK, code_rate, overhead, rolloff)
