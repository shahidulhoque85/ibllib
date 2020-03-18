import numpy as np
import brainbox as bb
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import alf.io as ioalf
from oneibl.one import ONE
from ibllib.io import spikeglx

# Download data
one = ONE()
eid = one.search(subject='ZM_2240', date_range=['2020-01-23', '2020-01-23'])
lf_path = one.load(eid[0], dataset_types=['ephysData.raw.lf', 'ephysData.raw.meta',
                                          'ephysData.raw.ch'],
                   download_only=True)[0]

# Read in data
raw = spikeglx.Reader(lf_path)
signal = raw.read(nsel=slice(None, 100000, None), csel=slice(None, None, None))[0]
signal = np.rot90(signal)

# %% Calculate power spectrum and coherence between two random channels

ps_freqs, ps = bb.lfp.power_spectrum(signal, fs=raw.fs)
random_ch = np.random.choice(raw.nc, 2)
coh_freqs, coh, phase_lag = bb.lfp.coherence(signal[random_ch[0], :],
                                             signal[random_ch[1], :], fs=raw.fs)

# %% Create power spectrum and coherence plot

fig = plt.figure(figsize=(18, 12))
gs = GridSpec(2, 2, figure=fig)
cmap = sns.cubehelix_palette(dark=1, light=0, as_cmap=True)

ax1 = fig.add_subplot(gs[:, 0])
sns.heatmap(data=np.log10(ps[:, ps_freqs < 140]), cbar=True, ax=ax1, yticklabels=50,
            cmap=cmap, cbar_kws={'label': 'log10 power ($V^2$)'})
ax1.set(xticks=np.arange(0, np.sum(ps_freqs < 140), 50),
        xticklabels=np.array(ps_freqs[np.arange(0, np.sum(ps_freqs < 140), 50)], dtype=int),
        ylabel='Channels', xlabel='Frequency (Hz)')


ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(ps_freqs, ps[random_ch[0], :])
ax2.set(xlim=[1, 140], yscale='log', ylabel='Power ($V^2$)',
        xlabel='Frequency (Hz)', title='Channel %d' % random_ch[0])

ax3 = fig.add_subplot(gs[1, 1])
ax3.plot(coh_freqs, coh)
ax3.set(xlim=[1, 140], ylabel='Coherence', xlabel='Frequency (Hz)',
        title='Channel %d and %d' % (random_ch[0], random_ch[1]))

plt.tight_layout(pad=5)

# %% Create
