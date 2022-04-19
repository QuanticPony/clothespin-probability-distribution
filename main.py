import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as Animation

class pinzas_simulation:
    def __init__(self, n_pinzas, length, width, histogram_bins):
        self.n_pinzas = n_pinzas
        self.length = length
        self.width = width
        self.histogram_bins = histogram_bins
        
        self.pinzas = np.linspace(0, self.length-self.width, self.n_pinzas)
        
        self.init_histogram()
        
    def init_histogram(self):
        self.histogram = np.zeros(self.histogram_bins)
        self._counts = 0
        self.histogram_delta = self.length/self.histogram_bins
        self.bins = (np.arange(self.histogram_bins) + 0.5)*self.histogram_delta

    def get_histogram(self):
        return self.histogram[:] / (np.sum(self.histogram) * self.histogram_delta)

    def update_histogram(self, positions):
        self.histogram[np.floor((positions+self.width/2)/self.histogram_delta).astype(int)] += 1
        self._counts += 1
            
    def plot_histogram(self, ax):
        ax.bar(self.bins, self.get_histogram(), width=self.histogram_delta)
    
    def new_pinzas(self):
        for i in range(self.n_pinzas):
            self.pinzas[i] += (2*np.random.random()-1) * 2 * self.width
            
            left = self.pinzas[i-1] + self.width if (i-1)>=0 else 0
            right = self.pinzas[i+1] - self.width if (i+1)<self.n_pinzas else self.length-self.width
            
            colide = True
            while colide:
                colide = False
                if left > self.pinzas[i]:
                    self.pinzas[i] = 2*left - self.pinzas[i]
                    colide = True

                if right < self.pinzas[i]:
                    self.pinzas[i] = 2*right - self.pinzas[i]
                    colide = True
            
        return self.pinzas
        
    def plot_pinzas(self, ax):
        ax.set_title('Clothes pin')
        ax.bar(self.pinzas+self.width/2, np.ones(self.n_pinzas), width=self.width*0.9, color='brown')
        
    def prepare_canvas(self, fig, ax_histogram, ax_pinzas):
        self.ax_histogram = ax_histogram
        self.ax_pinzas = ax_pinzas
        self.fig = fig
        
        self.ax_pinzas.set_title('Clothes pin')
        self.ax_pinzas.set_ylabel('')
        self.ax_pinzas.set_xlabel('Position')
        self.ax_histogram.set_title('Histogram')
        self.ax_histogram.set_xlabel('Position')
        self.ax_histogram.set_ylabel('Relative frequency')
        
    def prepare_animation(self, steps_per_frame=1):
        self.steps_per_frame = steps_per_frame
        self.animation = Animation.FuncAnimation(self.fig, self.update_plots, interval=50)
    
    def update_plots(self, *args, iterations=None,**kargs):
        if iterations is None:
            iterations = self.steps_per_frame
        for _ in range(iterations):
            self.update_histogram(self.new_pinzas())
        self.ax_histogram.clear()
        self.ax_pinzas.clear()
        
        self.ax_pinzas.set_title('Clothes pin')
        self.ax_pinzas.set_ylabel('')
        self.ax_pinzas.set_xlabel('Position')
        self.ax_histogram.set_title('Histogram')
        self.ax_histogram.set_xlabel('Position')
        self.ax_histogram.set_ylabel('Relative frequency')
        
        self.ax_histogram.set_xlim((0,self.length))
        self.ax_pinzas.set_xlim((0,self.length))
        self.plot_histogram(self.ax_histogram)
        self.plot_pinzas(self.ax_pinzas)
        
    

def main():
    sim = pinzas_simulation(15, 2, 0.1, 200)
    
    fig, (ax1, ax2) = plt.subplots(nrows=2)
    
    sim.prepare_canvas(fig, ax2, ax1)
    sim.prepare_animation(steps_per_frame=1000)
    # sim.update_plots(iterations=int(1e5))
    plt.show()
    
    
if __name__=='__main__':
    main()