from mayavi import mlab
from tvtk.api import tvtk

def auto_sphere(image_file):
    fig = mlab.figure(size=(600, 600))
    img = tvtk.JPEGReader()
    img.file_name = image_file
    img.update()  # Ensure the image is read
    
    texture = tvtk.Texture(input_connection=img.output_port, interpolate=1)
    
    sphere = tvtk.SphereSource(radius=2, theta_resolution=100, phi_resolution=100)
    sphere_mapper = tvtk.PolyDataMapper(input_connection=sphere.output_port)
    sphere_actor = tvtk.Actor(mapper=sphere_mapper, texture=texture)
    
    fig.scene.add_actor(sphere_actor)
    return fig

if __name__ == "__main__":
    image_file = r"C:\Users\Kshit\Desktop\extensiontask\bluemarble.jpg"
    fig = auto_sphere(image_file)
    
    print("Input Start Location Vector: ")
    x = float(input("X: "))
    y = float(input("Y: "))
    z = float(input("Z: "))
    D = (x**2 + y**2 + z**2)**0.5
    x = [x / D]
    y = [y / D]
    z = [z / D]

    print("Input Speed vector: ")
    a = float(input("X: "))
    b = float(input("Y: "))
    c = float(input("Z: "))

    vx = [a]
    vy = [b]
    vz = [c]

    ax = 0
    ay = 0
    az = 0
    dt = 0.02

    n = 0
    t = [0]

    while D >= 1 and n <= 5000:
        D = (x[n]**2 + y[n]**2 + z[n]**2)**0.5
        g = (6.67 * 10**-11 * 5.972 * 10**24) / ((D * 6371000)**2)
        ax = (x[n] / D) * -g
        ay = (y[n] / D) * -g
        az = (z[n] / D) * -g

        x.append(x[n] + vx[n] * dt + 0.5 * ax * dt**2)
        y.append(y[n] + vy[n] * dt + 0.5 * ay * dt**2)
        z.append(z[n] + vz[n] * dt + 0.5 * az * dt**2)

        vx.append(vx[n] + ax * dt)
        vy.append(vy[n] + ay * dt)
        vz.append(vz[n] + az * dt)

        t.append(t[n] + dt)

        n += 1

    mlab.plot3d(x, y, z, tube_radius=0.01)

    # Reset initial conditions for the second loop
    x = [x[0]]
    y = [y[0]]
    z = [z[0]]

    vx = [a]
    vy = [b]
    vz = [c]

    n = 0
    t = [0]

    while D >= 1 and n <= 5000:
        D = (x[n]**2 + y[n]**2 + z[n]**2)**0.5
        g = (6.67 * 10**-11 * 5.972 * 10**24) / ((D * 6371000)**2)
        ax = (x[n] / D) * -g
        ay = (y[n] / D) * -g
        az = (z[n] / D) * -g

        d1 = (x[n]**2 + y[n]**2)**0.5
        cory = -2 * 3.14 * d1 * (x[n] / d1) * 7.29211e-5 * dt * 6371 * 0.3
        corx = 2 * 3.14 * d1 * (y[n] / d1) * 7.29211e-5 * dt * 6371 * 0.3
        print(corx, cory, d1)

        x.append(corx + x[n] + vx[n] * dt + 0.5 * ax * dt**2)
        y.append(cory + y[n] + vy[n] * dt + 0.5 * ay * dt**2)
        z.append(z[n] + vz[n] * dt + 0.5 * az * dt**2)

        vx.append(vx[n] + ax * dt)
        vy.append(vy[n] + ay * dt)
        vz.append(vz[n] + az * dt)

        t.append(t[n] + dt)

        n += 1

    mlab.plot3d(x, y, z, tube_radius=0.01, color=(1, 0, 0))

    mlab.show()
