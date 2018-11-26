"""plotter module

Provide functions to generate some useful plots.
"""
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def network(net):
    pos=nx.circular_layout(net)
    nx.draw_networkx(net,pos)
    return plt

def network_tip_states(net, x):
    '''The state given of the tipping_network is plotted.
    Tipped tipping elements are red, non-tipped elements are green.'''
    tip_state = net.get_tip_states(x)
    color_map = []
    label_dict = {}
    for node in range(net.number_of_nodes()):
        label_dict.update({node: str(node) + ' (' +
                           net.get_node_types()[node] + ')'})
        if tip_state[node]:
            color_map.append('red')
        else:
            color_map.append('green')
    
    nx.draw_networkx(net, node_color=color_map, labels=label_dict,
                     arrows=True, fond_size=10)
    return plt

def series(t, x, legend=False):
    for i in range(x.shape[1]):
        plt.plot(t, x[:,i], label='$x_'+str(i+1)+'$')
    if legend:
        plt.legend(bbox_to_anchor=(0.2, 0.9), loc=1, borderaxespad=0.)
    plt.xlabel('time')
    plt.ylabel('$x$')
    return plt

def phase_flow(net, xrange, yrange):
    if not net.number_of_nodes() == 2:
        raise ValueError("Function only supported for two-element networks!")
    x,y = np.meshgrid(np.linspace(xrange[0],xrange[1],21), 
                      np.linspace(yrange[0],yrange[1],21))
    
    u, v = np.zeros(x.shape), np.zeros(y.shape)
    n_x , n_y = x.shape
    
    for idx in range(n_x):
        for idy in range(n_y):
            x_val = x[idx,idy]
            y_val = y[idx,idy]
            f = net.f([x_val,y_val], 0)
            u[idx,idy] = f[0]
            v[idx,idy] = f[1]
            
    plt.streamplot(x, y, u, v, color='black')
    return plt

def phase_space(net, xrange, yrange):
    if not net.number_of_nodes() == 2:
        raise ValueError("Function only supported for two-element networks!")
    x,y = np.meshgrid(np.linspace(xrange[0],xrange[1],101), 
                      np.linspace(yrange[0],yrange[1],101))
    r = np.zeros(x.shape)
    n_x , n_y = x.shape
    
    for idx in range(n_x):
        for idy in range(n_y):
            x_val = x[idx,idy]
            y_val = y[idx,idy]
            f = net.f([x_val,y_val], 0)
            r[idx,idy] = np.sqrt(pow(f[0],2)+pow(f[1],2))
            
    plt.contourf(x, y, r, 25)
    return plt

def stability(net,xrange,yrange):
    if not net.number_of_nodes() == 2:
        raise ValueError("Function only supported for two-element networks!")
    x,y = np.meshgrid(np.linspace(xrange[0],xrange[1],201), 
                      np.linspace(yrange[0],yrange[1],201))

    stability = np.zeros(x.shape)
    n_x , n_y = x.shape
    
    for idx in range(n_x):
        for idy in range(n_y):
            x_val = x[idx,idy]
            y_val = y[idx,idy]
            val, vec = np.linalg.eig(net.jac([x_val,y_val],0))
            stable = np.less(val,[0,0])
            
            stability[idx,idy] = sum(stable)
    
    colors = [(0.8, 0.1, 0.1), (0.9, 0.9, 0), (0.1, 0.1, 0.8)]
    cmp = LinearSegmentedColormap.from_list('mylist', colors, N=3)        
    plt.contourf(x, y, stability,levels=[-0.5,0.5,1.5,2.5],cmap=cmp)

    plt.colorbar(ticks=[0,1,2])
    return plt

def cascade_size(csv_file, x_var, y_var, par):
    # local pandas import
    import pandas as pd
    
    df = pd.read_csv(csv_file)
    df_random = df
    
    x_vars = np.sort(df_random[x_var])
    x_vars = np.unique( x_vars.round(decimals=4) )
    par_vals = np.sort(df_random[par].unique())

    for p in par_vals:
        rows = df_random.loc[df_random[par] == p]
        cascade_size = np.array([])
        cascade_size_stderr = np.array([])
        for x in x_vars:
            x_rows = rows[rows[x_var].apply(np.isclose, b=x, atol=0.001)]
            cascade_size = np.append(cascade_size,
                                     x_rows[y_var].mean())
            cascade_size_stderr = np.append(cascade_size_stderr,
                                            stats.sem(x_rows[y_var]))
    
        mask = np.isfinite(cascade_size)
        plt.errorbar(x_vars[mask], 
                     cascade_size[mask],
                     yerr = cascade_size_stderr[mask],
                     xerr = None,
                     fmt='x-',
                     capsize=3,
                     label=p)
    
    return plt

"""   
        x_end[basin_number].append(ev.states[-1][0])
        y_end[basin_number].append(ev.states[-1][1])         
        x_init[basin_number].append(x)
        y_init[basin_number].append(y)
        equilibria[basin_number] = [np.mean(x_end[basin_number]), np.mean(y_end[basin_number])]

    plt.xlim(xrange[0], xrange[1])
    plt.ylim(yrange[0], yrange[1])
    for basin in enumerate(equilibria):
        plt.scatter(x_init[basin[0]] , y_init[basin[0]])
        
    x_val = [x[0] for x in equilibria]
    y_val = [x[1] for x in equilibria]
    plt.scatter(x_val,y_val,c='black')
    plt.xlabel('$x_1$', fontsize=15)
    plt.ylabel('$x_2$', fontsize=15)
    plt.title('$d=2$', fontsize=15)
    plt.show()
    """