# Functional Brain Imaging Systems: Programming Assignments

Programming assignments for the graduate-level course **Functional Brain Imaging Systems**. The repository contains two main projects:

## Project 1: Forward and Inverse Modeling of EEG and MEG

This project simulates EEG and MEG measurements from a known source and then tests whether that source can be recovered.

### Forward modeling (`EEG_MEG_forward.ipynb`)

- Generates the locations of the scalp sensors and the dipoles.
- Computes the **lead field matrix** using a **spherical head model**.
- Selects one dipole and assigns it a current vector.
- Calculates the resulting EEG and MEG measurements.

### Inverse modeling (`EEG_MEG_inverse.ipynb`)

- Uses the quantities generated in the forward step (sensor and dipole locations, lead field, simulated measurements).
- Solves the inverse problem to check whether the true source can be correctly localized.

## Project 2: ERP Extraction and Topographic Maps

This project works through the analysis of real, event-related EEG data using the [MNE-Python](https://mne.tools/) library. The workflow follows an iterative cycle of preprocessing, visualization, and quality assessment.

### Workflow

1. **Load** the EEG dataset into Python.
2. **Preprocess** the data:
   - Remove non-EEG channels.
   - Apply filters to remove non-brain activity.
   - Resample the data if needed to make computation more efficient.
3. **Compute and visualize** the brain's response to specific events:
   - Event-Related Potentials (ERPs).
   - Corresponding topographic maps (topomaps).
4. **Assess data quality** by checking the plots for clear patterns and for signs of noise or artifacts.
5. **Refine the preprocessing** if the data is not yet clean, for example by:
   - Interpolating bad channels.
   - Rejecting noisy trials (epochs).
6. **Repeat** steps 3 to 5 until the ERPs are clear and interpretable and the topomaps are reasonable.