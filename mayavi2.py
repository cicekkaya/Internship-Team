import numpy as np
import rasterio
import mayavi.mlab as mlab

class MyMayAvi:
    coordinate_text = None
    selected_rectangle = None
    #output_file = "C:/Users/stj.rnozdemir/Desktop/Copy3.dt2"
    dted_file_path = "C:/Users/stj.fbkuzucu/Desktop/Copy3.dt2"

    def __init__(self):
        self.actor = None

    def __call__(self, *args, **kwargs):

        def cont(event):
            if event.actor is mesh.actor.actor:
                # Seçilen noktanın koordinatlarını al
                x, y, z = event.pick_position
                print(x,y)

        def on_pick(event):
            if event.actor is mesh.actor.actor:
                # Seçilen noktanın koordinatlarını al
                x, y, z = event.pick_position

                # Koordinatları coğrafi koordinatlara dönüştür
                longitude, latitude = src.xy(y, x)

                # Önceki metni sil
                if MyMayAvi.coordinate_text:
                    MyMayAvi.coordinate_text.remove()

                # Yeni metni ekrana yazdır
                MyMayAvi.coordinate_text = mlab.text(x=x, y=y, z=z,
                                            text=f"Latitude: {latitude:.6f}\nLongitude: {longitude:.6f}\nElevation: {z:.2f}",
                                            width=0.1, color=(0, 0, 0))


                # Eski dikdörtgeni sil
                if MyMayAvi.selected_rectangle:
                    MyMayAvi.selected_rectangle.remove()

                # Yeni dikdörtgeni oluştur ve göster
                width = 100  # Width of the rectangle
                height = 100  # Height of the rectangle
                rect_center_x = x
                rect_center_y = y
                rect_height_above_terrain = 50  # Adjust this value as needed to lift the rectangle above the terrain
                MyMayAvi.selected_rectangle = mlab.plot3d(
                    [rect_center_x - width / 2, rect_center_x + width / 2, rect_center_x + width / 2,
                     rect_center_x - width / 2, rect_center_x - width / 2],
                    [rect_center_y - height / 2, rect_center_y - height / 2, rect_center_y + height / 2,
                     rect_center_y + height / 2, rect_center_y - height / 2],
                    [z + rect_height_above_terrain, z + rect_height_above_terrain, z + rect_height_above_terrain,
                     z + rect_height_above_terrain, z + rect_height_above_terrain],
                    color=(1, 0, 0), tube_radius=None)

                # Zoom to the selected region
                mlab.view(azimuth=0, elevation=0, distance=300,
                          focalpoint=(rect_center_x, rect_center_y, z))  # Set the focal point to the center of the rectangle

                find_elevation_at_coordinate(self.dted_file_path, longitude, latitude)

        def find_elevation_at_coordinate(file_path, longitude, latitude):
            print("find_elev çalıştı!")
            with rasterio.open(file_path, 'r+') as dataset:
                row, col = dataset.index(longitude, latitude)
                elevation_data = dataset.read(1)
                print("Önceki yükseklik:", elevation_data[row, col])
                print("Koordinat: (row={}, col={})".format(row, col))

                # Kare şeklindeki bölgenin boyutunu belirleyin (örneğin 5x5)
                kare_boyutu = 100
                # Kare şeklindeki bölgeyi sınırlayın
                min_row = max(0, row - kare_boyutu // 2)
                max_row = min(dataset.height - 1, row + kare_boyutu // 2)
                min_col = max(0, col - kare_boyutu // 2)
                max_col = min(dataset.width - 1, col + kare_boyutu // 2)

                # Kare içindeki tüm noktaların yüksekliğini 2500 yapın
                for r in range(min_row, max_row + 1):
                    for c in range(min_col, max_col + 1):
                        elevation_data[r, c] += 300

                dataset.write_band(1, elevation_data)

            source = self.GetMesh()
            ms = source.mlab_source
            ms.reset()
            mlab.show()
            """mesh2 = self.GetMesh()
            mlab.show(mesh2)"""
            print("silindi")

            print("Yeni yükseklik:", elevation_data[row, col])



        with rasterio.open("C:/Users/stj.fbkuzucu/Desktop/Copy3.dt2") as src:
            elev = src.read(1)
            nrows, ncols = elev.shape
            print(np.arange(nrows))
            x, y = np.meshgrid(np.arange(ncols), np.arange(nrows))
            z = elev
            mesh = mlab.mesh(x, y, z * 0.1)
            mlab.gcf().on_mouse_pick(on_pick)
            mlab.gcf().on_mouse_pick(cont,button='Right')
            return mesh

    def GetMesh(self):
        with rasterio.open("C:/Users/stj.fbkuzucu/Desktop/Copy3.dt2") as src:
            elev = src.read(1)
            nrows, ncols = elev.shape
            print(np.arange(nrows))
            x, y = np.meshgrid(np.arange(ncols), np.arange(nrows))
            z = elev
            mesh = mlab.mesh(x, y, z * 0.1)
            return mesh