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


def baseline_vs_candidates_plotter(list_of_candidates, target_data, city, segment_class, segment_idx, display_row = 2, display_column = 5):
    idx_random = np.arange(1,len(list_of_candidates))
    np.random.shuffle(idx_random)
    shuffled_candidates = list_of_candidates[idx_random]
    count_plot = 1 
    max_count_plot = display_row*display_column
    y_target = np.array(target_data[city]).reshape(-1,1)[:,0]
    x_target = np.arange(0,len(y_target),1)
    plt.figure(figsize = (16,8))
    while count_plot <= max_count_plot:
        plt.subplot(display_row,display_column,count_plot)
        plt.plot(x_target, y_target, color = 'darkorange', label = 'Target Time Series')
        plt.plot(x_target, shuffled_candidates[count_plot-1], color = 'navy', label = 'Possible Candidate')
        plt.legend()
        count_plot += 1
    plt.tight_layout()
    plt.savefig(f'images/target_and_candidates_{city}_segment_class_{segment_class}_idx_{segment_idx}.png')





