def create_time_steps(length):
    return list(range(-length, 0))

def plot_timeseries(axes, plot_data):
    labels = ['History', 'True Future', 'Model Prediction']
    marker = ['.-', 'rx', 'go']
    time_steps = create_time_steps(plot_data[0].shape[0])

    for i, x in enumerate(plot_data):
        if i:
            axes.plot(plot_data[i], marker[i], markersize=10,
                    label=labels[i])
        else:
            axes.plot(time_steps, plot_data[i].flatten(), marker[i], label=labels[i])
    axes.legend()
    axes.set_xlim([time_steps[0], plot_data[1].size + 10])
    axes.set_xlabel('Time-Step')
    return axes