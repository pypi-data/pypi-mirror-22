# -*- coding: utf-8 -*-
"""
Created on Fri Feb  26 18:16:24 2015
DataBase de datos de consumo eléctrico
@author: Eugenio Panadero
"""
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator, HourLocator
# import seaborn as sns
from esiosdata.esios_config import TARIFAS, TARIFAS_DESC, COLS_PVPC
from esiosdata.importpvpcdata import pvpc_calc_tcu_cp_feu_d
# from matplotlib.ticker import MultipleLocator


__author__ = 'Eugenio Panadero'
__credits__ = ["Eugenio Panadero"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Eugenio Panadero"


UDS = '€/kWh'
COMPS_PLOT = ['PVPC',
              'MERCADO DIARIO E INTRADIARIO',
              'SERVICIOS DE AJUSTE',
              'PEAJE DE ACCESO',
              'PAGO POR CAPACIDAD',
              'SERVICIO DE INTERRUMPILIDAD',
              'FINANCIACIÓN OS',
              'FINANCIACIÓN OM']
TARIFAS_COL = dict(zip(TARIFAS, ['#dd4b39', '#1aa2d8', '#76b823']))

P_1 = [[0.86666667, 0.29411765, 0.22352941, 1.],
       [0.88621366, 0.39760172, 0.33736189, 1.],
       [0.90622605, 0.5035497, 0.45390467, 1.],
       [0.92577304, 0.60703377, 0.56773714, 1.],
       [0.94578544, 0.71298174, 0.68427992, 1.],
       [0.96579784, 0.81892972, 0.80082269, 1.],
       [0.98534483, 0.92241379, 0.91465517, 1.]]
P_2 = [[0.10196078, 0.63529412, 0.84705882, 1.],
       [0.2351721, 0.6899185, 0.87047957, 1.],
       [0.37155512, 0.74584346, 0.89445795, 1.],
       [0.50476644, 0.80046784, 0.91787869, 1.],
       [0.64114946, 0.85639281, 0.94185707, 1.],
       [0.77753248, 0.91231777, 0.96583545, 1.],
       [0.9107438, 0.96694215, 0.9892562, 1.]]
P_3 = [[0.4627451, 0.72156863, 0.1372549, 1.],
       [0.54363812, 0.76479563, 0.26551579, 1.],
       [0.62645716, 0.80905184, 0.39683051, 1.],
       [0.70735018, 0.85227884, 0.5250914, 1.],
       [0.79016922, 0.89653505, 0.65640612, 1.],
       [0.87298826, 0.94079127, 0.78772084, 1.],
       [0.95388128, 0.98401826, 0.91598174, 1.]]
TARIFAS_PALETTES = dict(zip(TARIFAS, [P_1, P_2, P_3]))
FIGSIZE = (18, 10)


# MAKE DATA AS WEB: https://www.esios.ree.es/es/pvpc?date=22-02-2016
def _prep_pvpc_data_for_plot_web_esios(df):
    return pvpc_calc_tcu_cp_feu_d(df.copy(), verbose=False, convert_kwh=True).tz_localize(None).sort_index()


def pvpcplot_fill_tarifa(df, tarifa=TARIFAS[0], ax=None, show=True, ymax=None):
    df = _prep_pvpc_data_for_plot_web_esios(df)
    data_p = df[[c + tarifa for c in COLS_PVPC]]
    if ax is None:
        fig, ax = plt.subplots(figsize=(14, 10))
    # sns.set_style("whitegrid")
    # colors = list(reversed(sns.light_palette(TARIFAS_COL[tarifa], n_colors=7)))
    colors = TARIFAS_PALETTES[tarifa]
    init = np.zeros(len(data_p.index))
    for c, label, col in zip(list(data_p.columns)[1:-1], COMPS_PLOT[1:], colors):
        ax.fill_between(data_p.index, data_p[c].values + init, init, color=col, label=label)
        init = data_p[c].values + init
    ax.plot(data_p.index, data_p[tarifa].values, color=colors[0], label=COMPS_PLOT[0], lw=2)
    if ymax is not None:
        ax.set_ylim([0, ymax])
    ax.yaxis.label.set_text('{} [{}]'.format(TARIFAS_DESC[tarifa], UDS))
    if len(df) < 30:
        ax.xaxis.set_major_formatter(DateFormatter('%H'))
        ax.xaxis.set_major_locator(HourLocator(byhour=range(0, 24, 2)))  # byhour=4)) #MultipleLocator(4)), tz=TZ
    ax.grid(axis='y', color='grey', linestyle='--', linewidth=.5)
    ax.grid(axis='x', b='off')
    ax.set_axisbelow(False)
    ax.legend(fontsize='x-small', loc=3, frameon=True, framealpha=.6, ncol=2, borderaxespad=1.)
    if show:
        plt.show()


def pvpcplot_tarifas_hora(df, ax=None, show=True, ymax=None, fs=FIGSIZE):
    df = _prep_pvpc_data_for_plot_web_esios(df)
    if ax is None:
        fig, ax = plt.subplots(figsize=fs)
    # sns.set_style("whitegrid")
    for k in TARIFAS:
        ax.plot(df.index, df[k].values, color=TARIFAS_COL[k], label=TARIFAS_DESC[k], lw=4)
    if ymax is not None:
        ax.set_ylim([0, ymax])
    if len(df) < 30:
        ax.xaxis.set_major_formatter(DateFormatter('%H'))
        ax.xaxis.set_major_locator(HourLocator(byhour=range(len(df))))  # byhour=4)) #MultipleLocator(4)), tz=TZ
    ax.grid(axis='x', b='off')
    ax.grid(axis='y', color='grey', linestyle='--', linewidth=.5)
    ax.set_axisbelow(False)
    ax.legend(loc=0, fontsize='large', frameon=True, framealpha=.8)
    if show:
        plt.show()


# PLOT FIGURE 1x3 + 3
def pvpcplot_grid_hora(df_day, fs=FIGSIZE):
    df_day = _prep_pvpc_data_for_plot_web_esios(df_day)
    ymax = np.ceil(df_day[TARIFAS].max().max() / .02) * .02
    plt.figure(figsize=fs)
    ax1 = plt.subplot2grid((2, 3), (0, 0), colspan=3)
    axes = [plt.subplot2grid((2, 3), (1, x)) for x in [0, 1, 2]]
    pvpcplot_tarifas_hora(df_day, ax=ax1, show=False, ymax=ymax)
    for a, k in zip(axes, TARIFAS):
        pvpcplot_fill_tarifa(df_day, tarifa=k, ax=a, show=False, ymax=ymax)
    plt.show()


# SCATTER PLOT EV. PVPC
def pvpcplot_ev_scatter(pvpc_mean_daily, pvpc_mean_monthly, tarifa=TARIFAS[0],
                        superposic_anual=True, ax=None, plot=True):
    if ax is None:
        fig, ax = plt.subplots(figsize=FIGSIZE)
    # sns.set_style("whitegrid")

    pvpc_diario = pvpc_mean_daily[tarifa]
    pvpc_mensual = pvpc_mean_monthly[tarifa]
    if superposic_anual:
        base_t = pd.Timestamp(dt.datetime(year=dt.datetime.now().year, month=1, day=1), tz='Europe/Madrid')
        gr_dia = pvpc_diario.groupby(lambda idx: idx.year)
        try:
            # noinspection PyPackageRequirements
            import seaborn as sns
            cols = sns.light_palette(TARIFAS_COL[tarifa], n_colors=len(gr_dia) + 2)[2:]
        except ImportError:
            sns = None
            cols = TARIFAS_PALETTES[tarifa]

        for group_d, group_m, color in zip(gr_dia, pvpc_mensual.groupby(lambda idx: idx.year), cols):
            year, df_d = group_d
            year_m, df_m = group_m
            assert(year == year_m)
            delta = base_t - pd.Timestamp(dt.datetime(year=year, month=1, day=1), tz='Europe/Madrid')
            ax.scatter(df_d.index + delta, df_d.values, label='PVPC_{} diario ({})'.format(tarifa, year), color=color)
            ax.plot(df_m.index + delta + pd.Timedelta(days=14), df_m.values,
                    label='PVPC_{} mensual ({})'.format(tarifa, year), color=color, lw=5, ls=':')
        ax.xaxis.set_major_formatter(DateFormatter('%b'))
        ax.xaxis.set_major_locator(MonthLocator())
        plt.xlim(base_t, pd.Timestamp(dt.datetime(year=base_t.year + 1, month=1, day=1), tz='Europe/Madrid'))
    else:
        # envolv_dia = pvpc_diario.tz_localize(None).resample('W', how=[np.min, np.max, np.argmax, np.argmin])
        envolv_dia = pvpc_diario.tz_localize(None).resample('W').apply([np.min, np.max, np.argmax, np.argmin])
        x = envolv_dia['argmax'].tolist() + envolv_dia['argmin'].tolist()[::-1]
        y = envolv_dia['amax'].tolist() + envolv_dia['amin'].tolist()[::-1]
        ax.fill(x, y, color=TARIFAS_COL[tarifa], alpha=.25)
        ax.scatter(pvpc_diario.index, pvpc_diario.values,
                   label='PVPC_{} diario'.format(tarifa), color=TARIFAS_COL[tarifa])
        ax.plot(pvpc_mensual.index + pd.Timedelta(days=14), pvpc_mensual.values,
                label='PVPC_{} mensual'.format(tarifa), color=TARIFAS_COL[tarifa], lw=6)
        ax.xaxis.set_major_formatter(DateFormatter("%b'%y"))
        ax.xaxis.set_major_locator(MonthLocator(interval=2))
    ax.grid(color='grey', linestyle='--', linewidth=.5)
    ax.legend(loc='best', fontsize='large', frameon=True, framealpha=.7)
    if plot:
        plt.show()
