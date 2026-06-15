import streamlit as st
from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt

st.set_page_config(page_title="Futbol Analiz", layout="wide")
st.title("⚽ Euro 2024 — Shot Map")

# Maç listesini çek
maclar = sb.matches(competition_id=55, season_id=282)
maclar['label'] = maclar['home_team'] + ' vs ' + maclar['away_team']

secim = st.selectbox("Maç seç:", maclar['label'].tolist())

secilen_mac = maclar[maclar['label'] == secim].iloc[0]
mac_id = secilen_mac['match_id']

# Veriyi çek
olaylar = sb.events(match_id=mac_id)
sutlar = olaylar[olaylar['type'] == 'Shot'].copy()

# Grafik çiz
pitch = Pitch(pitch_color='#1a1a2e', line_color='white')
fig, ax = pitch.draw(figsize=(14, 9))
fig.set_facecolor('#1a1a2e')

for _, sut in sutlar.iterrows():
    x = sut['location'][0]
    y = sut['location'][1]
    xg = sut['shot_statsbomb_xg']
    sonuc = sut['shot_outcome']
    takim = sut['team']
    oyuncu = sut['player'].split()[-1]

    ev_takim = secilen_mac['home_team']
    renk = '#FF0000' if takim == ev_takim else '#FFFFFF'
    marker = '*' if sonuc == 'Goal' else 'o'
    boyut = xg * 2000 if sonuc == 'Goal' else xg * 800

    pitch.scatter(x, y, ax=ax, s=boyut, color=renk,
                  alpha=0.9, marker=marker,
                  edgecolors='yellow' if sonuc == 'Goal' else 'gray',
                  linewidth=1.5)

    if sonuc == 'Goal':
        ax.text(x, y + 3, oyuncu, color='yellow',
                fontsize=9, ha='center', fontweight='bold')

ev_xg = sutlar[sutlar['team'] == secilen_mac['home_team']]['shot_statsbomb_xg'].sum()
dep_xg = sutlar[sutlar['team'] == secilen_mac['away_team']]['shot_statsbomb_xg'].sum()

fig.text(0.5, 0.02,
         f"{secilen_mac['home_team']} xG: {ev_xg:.2f}    |    {secilen_mac['away_team']} xG: {dep_xg:.2f}",
         color='white', fontsize=12, ha='center',
         bbox=dict(boxstyle='round', facecolor='#2d2d4e', alpha=0.8))

plt.title(f"{secilen_mac['home_team']} vs {secilen_mac['away_team']} — Shot Map",
          color='white', fontsize=14, pad=15)

st.pyplot(fig)
