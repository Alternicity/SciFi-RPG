#scalar_field.py

import numpy as np
import matplotlib.pyplot as plt

# Toggle this to enable/disable the module
RUN_SCALAR_FIELD = False

if not RUN_SCALAR_FIELD:
    print("[SCALAR FIELD] Module disabled. Skipping scalar field visualization.")
    exit()
    
if __name__ == "__main__":
    mode = "3D"  # Change to "2D" to run the original field

    if mode == "2D":
        def temperature_field(x, y):
            return np.sin(x) * np.cos(y)

        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)

        Z = temperature_field(X, Y)

        plt.contourf(X, Y, Z, levels=50, cmap='plasma')
        plt.colorbar(label='Temperature')
        plt.title("2D Scalar Field: Temperature")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()

        #usage from terminal
        #python scalar_field.py

    elif mode == "3D":
        # Constants
        sqrt10 = np.sqrt(10)         # ~3.162277
        phi = (1 + np.sqrt(5)) / 2   # ~1.618034

        # Define the harmonic scalar field
        def harmonic_field(x, y):
            # Combine sinusoids modulated by √10 and phi
            return np.sin(sqrt10 * x) * np.cos(phi * y) + np.cos(x * y / sqrt10)

        # Generate grid
        x = np.linspace(-5, 5, 150)
        y = np.linspace(-5, 5, 150)
        X, Y = np.meshgrid(x, y)
        Z = harmonic_field(X, Y)

        # Plot
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
        ax.set_title("3D Harmonic Scalar Field (√10 + Phi)")
        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")
        ax.set_zlabel("Resonance")

        plt.tight_layout()
        plt.show()