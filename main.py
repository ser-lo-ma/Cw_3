

# Load the image Slphan.npy
f_true = np.load('SLphan.npy')


# Compute the Radon transform of the image
# Create volume geometries
v, h = f_true.shape
vol_geom = astra.create_vol_geom(v, h)

# Create projection geometries
angles = np.linspace(0, np.pi, 180, False)
proj_geom = astra.create_proj_geom('parallel', 1.0, h, angles)
# h should be the detector counts (number of detector pixels in a single projection or in other words the
# ”number of projection samples”)
# Create projector
proj_id = astra.create_projector('strip', proj_geom, vol_geom)
# Create sinogram
sinogram_id, sinogram = astra.create_sino(f_true, proj_id)

# Display the sinogram
plt.imshow(sinogram, cmap='gray')
plt.show()

# Reconstruct the image from the sinogram
# Create a data object for the reconstruction
rec_id = astra.data2d.create('-vol', vol_geom)
# Set up the algorithm object (unfiltered backprojection)
cfg = astra.astra_dict('BP')
cfg['ReconstructionDataId'] = rec_id
cfg['ProjectionDataId'] = sinogram_id
cfg['ProjectorId'] = proj_id
# Create the algorithm object from the configuration structure
alg_id = astra.algorithm.create(cfg)
# Run the algorithm
astra.algorithm.run(alg_id)
f_rec = astra.data2d.get(rec_id)

# Display the reconstructed image
plt.imshow(f_rec, cmap='gray')
plt.show()

# Now with a filtered backprojection
# Reconstruct the image from the sinogram
# Create a data object for the reconstruction
rec_id = astra.data2d.create('-vol', vol_geom)
# Set up the algorithm object (filtered backprojection)
cfg = astra.astra_dict('FBP')
cfg['ReconstructionDataId'] = rec_id
cfg['ProjectionDataId'] = sinogram_id
cfg['ProjectorId'] = proj_id
# Create the algorithm object from the configuration structure
alg_id = astra.algorithm.create(cfg)
# Run the algorithm
astra.algorithm.run(alg_id)
f_rec_2 = astra.data2d.get(rec_id)

# Display the reconstructed image
plt.imshow(f_rec_2, cmap='gray')
plt.show()

# Add noise to the sinogram and reconstruct the image
# Add noise to the sinogram
gNoisy = astra.functions.add_noise_to_sino(sinogram, 1000)
gNoisy_id = astra.data2d.create('-sino', proj_geom, gNoisy)

#Display the noisy sinogram
plt.imshow(gNoisy, cmap='gray')
plt.show()

# Reconstruct the image from the noisy sinogram
# Set up the algorithm object (filtered backprojection)
cfg = astra.astra_dict('FBP')
cfg['ReconstructionDataId'] = rec_id
cfg['ProjectionDataId'] = gNoisy_id
cfg['ProjectorId'] = proj_id
# Create the algorithm object from the configuration structure
alg_id = astra.algorithm.create(cfg)
# Run the algorithm
astra.algorithm.run(alg_id)
f_rec_3 = astra.data2d.get(rec_id)

# Display the reconstructed image
plt.imshow(f_rec_3, cmap='gray')
plt.show()

