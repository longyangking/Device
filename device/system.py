import numpy as np 

class Point:
    def __init__(self, position, onsite_func):
        self.position = position
        self.onsite_func = onsite_func

    def get_onsite(self, t):
        return self.onsite_func(t)

class Link:
    def __init__(self, start_point, end_point, coupling_func):
        self.start_point = start_point
        self.end_point = end_point
        self.coupling_func = coupling_func

    def get_coupling(self, t):
        return self.coupling_func(t)

    def get_startpoint(self):
        return self.start_point

    def get_endpoint(self):
        return self.end_point


class System:
    def __init__(self, points=None, links=None):
        self.points = list()
        if points is not None:
            self.points = points
        
        self.links = list()
        if links is not None:
            self.links = links

    def add_point(self, point):
        self.points.append(point)

    def add_link(self, link):
        self.links.append(link)

    def get_hamiltonian(self, t):
        n_sites = len(self.points)
        hamiltonian = np.zeros((n_sites,n_sites))
        for i in range(n_sites):
            hamiltonian[i,i] = self.points[i].get_onsite(t)

        n_couplings = len(self.links)
        for i in range(n_couplings):
            start_point = self.links[i].get_startpoint()
            end_point = self.links[i].get_endpoint()
            start_index = None
            end_index = None
            for m in range(n_sites):
                if self.points[m] == start_point:
                    start_index = m
                if self.points[m] == end_point: 
                    end_index = m  
                if (start_index is not None) and (end_index is not None):
                    break
            start2end, end2start = self.links[i].get_coupling(t)
            hamiltonian[start_index,end_index] = end2start
            hamiltonian[end_index,start_index] = start2end

        return hamiltonian

    def get_points(self):
        return self.points

    def get_n_sites(self):
        return len(self.points)

    def get_links(self):
        return self.links      

    def __setitem__(self,name,value):
        pass

    def __getitem__(self,name):
        pass

    def __delitem__(self,name):
        pass