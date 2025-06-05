import matplotlib.pyplot as plt
import numpy as np


def target_and_baseline_plotter(target_data, bank_of_data, city, segment_class, segment_idx):
    x_target = np.array(target_data['datetime'])  # or .values
    y_target = np.array(target_data[city]).reshape(-1,1)[:,0]
    plt.subplot(2,1,1)
    plt.title(f'Target Segment, City = {city}, Segment Class = {segment_class}, Segment Index = {segment_idx}', fontsize = 12)
    plt.plot(x_target,y_target, color='darkorange')
    plt.xticks(rotation=45)
    x_candidates = np.array(bank_of_data['datetime'])  # or .values
    y_candidates = np.array(bank_of_data[city]).reshape(-1,1)[:,0]  # or .values
    plt.subplot(2,1,2)
    plt.title('Bank of Candidates', fontsize = 20)
    plt.plot(x_candidates,y_candidates, color='navy')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'images/target_and_bank_city_{city}_segment_class_{segment_class}_idx_{segment_idx}.png')