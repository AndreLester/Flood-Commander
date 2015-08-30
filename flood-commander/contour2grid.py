import os
import math
import fiona


class Terrain:
    
    def __init__(self, temp_dir='./temp'):
        self.xyz = []
        self.temp_dir = temp_dir
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
    def contour2xyz(self, shpfile, col, grid_size, bbox = None):
        """Generate xyz values from contour lines
        
        Takes a contour shapefile as an input file. Inserts extra linearly
        interpolated points at the intervals using the grid_size value and 
        stores the result in self.xyz. If the bounding box is specified all
        x,y values outside it is discarded.
           
        Args:
            shpfile (str): The input contour shapefile of type polylines.
            col (str): The name of the column with the value like 'HEIGHT'
            grid_size (Optional[int/float]): The pixel size of the grid.
                Also used to determine in which interval to insert extra 
                points.
            bbox (str): A path to a shapefile. The first record is used to
                determine the bounding box.
                   
        Returns:
            The grid size as a tuple.
            self.xyz are populated with the values
            
        """
        with fiona.open(shpfile) as sf:
            self.addpts = 0
            for i, line in enumerate(sf):
                pts = list(line['geometry']['coordinates'])
                x1, y1 = pts[0][0], pts[0][1]
                # Catch an strange inconsistancy where the coordinates are 
                # list of tuples within a list
                if type(x1) is tuple:
                    pts = list(line['geometry']['coordinates'][0])
                    x1, y1 = pts[0][0], pts[0][1]
                value = line['properties'][col]
                for j, pt in enumerate(pts):
                    if j == 0:
                        continue
                    x2, y2 = pt[0], pt[1]
                    length = ((x2-x1)**2+(y2-y1)**2)**0.5
                    sections = int(math.ceil(length/grid_size))
                    if sections > 1:
                        dx = (x2-x1)/sections
                        dy = (y2-y1)/sections
                        for k in range(sections):
                            if k == 0:
                                continue
                            self.addpts += 1
                            newx = x1+k*dx
                            newy = y1+k*dy
                            self.xyz.append([newx, newy, value])
                    self.xyz.append([x1, y1, value])
                    x1, y1 = x2, y2
        self.xyz.append([x1, y1, value])
        
        return(self.grid_dim(grid_size))
        
    def grid_dim(self, grid_size):
        """Calculates the dimensions of the grid for a particular cell size
        and returns it. The cell size (self.gridsize) is also set the the 
        given value"""
        
        pts = list(zip(*self.xyz))
        xlist, ylist = pts[0], pts[1]
        left, right = min(xlist), max(xlist)
        bottom, top = min(ylist), max(ylist)
        
        self.left = int(left/grid_size)*grid_size-grid_size
        self.right = int(right/grid_size)*grid_size+grid_size
        self.bottom = int(bottom/grid_size)*grid_size-grid_size
        self.top = int(top/grid_size)*grid_size+grid_size
        self.grid_size = grid_size
        xdim = int((right-left)/grid_size)
        ydim = int((top-bottom)/grid_size)
        
        del pts, xlist, ylist
        
        return(xdim, ydim)
        
    def writexyz(self):
        """ Writes self.xyz to a specified output file
        
        Args:
            ofile (str): Name output file. Willbe generated inside the 
                self.temp_dir directory
            
        """
        
        ofile = self.temp_dir+'/xyz.txt'
        with open(ofile, 'w') as fout:
            print('X\tY\tZ', file=fout)
            for p in self.xyz:
                print(str(p[0]), str(p[1]), str(p[2]), sep='\t', file=fout)
        
    def saga_batch(self):
        """Writes the batch processing file "batch_file" for processing by
        SAGA
        """
        
        batch_file = self.temp_dir+'/SAGA_batch.txt'       
        with open(batch_file, 'w') as fout:
            # First convert die xyz data file to a shapefile
            print('io_shapes 3', file = fout, end = ' ')
            print('-SHAPES '+ '"'+self.temp_dir+'/xyz.shp'+'"', 
                  file = fout, end = ' ')
            print('-FILENAME '+ '"', self.temp_dir+'/xyz.txt'+'"', 
                  file = fout)
            
            # We create a grid from the point data
            print('grid_spline 4', file = fout, end = ' ')
            print('-SHAPES "../temp/xyz.shp"', file = fout, end = ' ')
            print('-FIELD "Z"', file = fout, end = ' ')
            print('-USER_XMIN', str(self.left), file = fout, end = ' ')
            print('-USER_XMAX', str(self.right), file = fout, end = ' ')
            print('-USER_YMIN', str(self.bottom), file = fout, end = ' ')
            print('-USER_YMAX', str(self.top), file = fout, end = ' ')
            print('-USER_SIZE', str(self.grid_size), file = fout, end = ' ')
            print('-USER_GRID "../temp/temporary.sgrd"', file = fout)
            
            # Now the grid is clipped to a polygon
            print('shapes_grid 7', file = fout, end = ' ')
            print('-OUTPUT "../temp/Main_Grid.sgrd"', 
                  file = fout, end = ' ')
            print('-INPUT "../temp/temporary.sgrd"', 
                  file = fout, end = ' ')
            print('-POLYGONS "../input/shapefiles_proj/areapolygon.shp"', 
                  file = fout)
            
            # Export the grid as an image to view
            print('io_grid_image 0', file = fout, end = ' ')
            print('-GRID "../temp/Main_Grid.sgrd"', 
                  file = fout, end = ' ')
            print('-FILE "../temp/grid.png"', 
                  file = fout, end = ' ')
            #print('-COLOURING 0', file = fout, end = ' ')
            #print('-COL_PALETTE 0', file = fout)

if __name__ == '__main__':
    T = Terrain()
    t = T.contour2xyz('contours_clipped.shp','HEIGHT', 2)
    print(len(T.xyz), T.addpts)
    print(t)
    T.writexyz()
    print(T.grid_dim(2))
    T.saga_batch()
    